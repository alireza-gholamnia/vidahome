from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django_ratelimit.decorators import ratelimit

from .forms import SignUpForm
from .models import User
from .services import request_otp, verify_otp
from apps.common.sms import normalize_phone

LOGIN_OTP_PHONE_KEY = "login_otp_phone"
LOGIN_NEXT_URL_KEY = "login_next_url"
OTP_VERIFY_MAX_ATTEMPTS = 5
OTP_VERIFY_ATTEMPT_WINDOW_SECONDS = 300


def _json_login_response(success: bool, message: str = "", redirect_url: str = ""):
    return JsonResponse({"success": success, "message": message, "redirect": redirect_url})


def _default_redirect_for_user(user) -> str:
    return "/admin/" if user and user.is_superuser else "/panel/"


def _sanitize_next_url(request, raw_next: str, *, default: str) -> str:
    candidate = (raw_next or "").strip()
    if candidate and url_has_allowed_host_and_scheme(
        url=candidate,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return candidate
    return default


def _store_safe_next_url(request) -> None:
    raw_next = request.GET.get("next") or request.POST.get("next") or ""
    safe_next = _sanitize_next_url(request, raw_next, default="")
    if safe_next:
        request.session[LOGIN_NEXT_URL_KEY] = safe_next


def _resolve_safe_next_url(request, user) -> str:
    raw_next = (
        request.GET.get("next")
        or request.POST.get("next")
        or request.session.pop(LOGIN_NEXT_URL_KEY, None)
    )
    fallback = _default_redirect_for_user(user)
    safe_next = _sanitize_next_url(request, raw_next, default=fallback)
    if safe_next == "/":
        return fallback
    return safe_next


def _otp_verify_cache_key(request, phone: str) -> str:
    normalized_phone = normalize_phone(phone) or "unknown"
    ip = request.META.get("REMOTE_ADDR", "") or "unknown"
    return f"accounts:otp_verify_attempts:{ip}:{normalized_phone}"


def _otp_verify_is_limited(request, phone: str) -> bool:
    key = _otp_verify_cache_key(request, phone)
    attempts = int(cache.get(key, 0) or 0)
    return attempts >= OTP_VERIFY_MAX_ATTEMPTS


def _otp_verify_register_failure(request, phone: str) -> None:
    key = _otp_verify_cache_key(request, phone)
    attempts = int(cache.get(key, 0) or 0) + 1
    cache.set(key, attempts, OTP_VERIFY_ATTEMPT_WINDOW_SECONDS)


def _otp_verify_clear_failures(request, phone: str) -> None:
    cache.delete(_otp_verify_cache_key(request, phone))


@method_decorator(ratelimit(key="ip", rate="10/m", method="POST", block=True), name="post")
class PhoneLoginView(View):
    """ورود با موبایل - مرحله ۱: دریافت شماره و ارسال OTP"""

    def get(self, request):
        if request.user.is_authenticated:
            dest = "/admin/" if request.user.is_superuser else "/panel/"
            return redirect(dest)
        # اگر کاربر از صفحه تأیید کد برگشته، شماره قبلی را اتوفیل کن
        phone = request.session.get(LOGIN_OTP_PHONE_KEY, "")
        return render(
            request,
            "accounts/phone_login.html",
            {
                "breadcrumbs": [{"title": "صفحه اصلی", "url": "/"}, {"title": "ورود", "url": None}],
                "step": "phone",
                "phone": phone,
            },
        )

    def post(self, request):
        if request.user.is_authenticated:
            dest = _default_redirect_for_user(request.user)
            return redirect(dest)
        phone = (request.POST.get("phone") or "").strip()
        success, message = request_otp(phone)
        if success:
            request.session[LOGIN_OTP_PHONE_KEY] = normalize_phone(phone)
            _store_safe_next_url(request)
            return redirect("accounts:otp_verify")
        return render(
            request,
            "accounts/phone_login.html",
            {
                "breadcrumbs": [{"title": "صفحه اصلی", "url": "/"}, {"title": "ورود", "url": None}],
                "step": "phone",
                "phone": phone,
                "error": message,
            },
        )


@method_decorator(ratelimit(key="ip", rate="20/m", method="POST", block=True), name="post")
class OTPVerifyView(View):
    """ورود با موبایل - مرحله ۲: تأیید کد OTP"""

    def get(self, request):
        if request.user.is_authenticated:
            dest = "/admin/" if request.user.is_superuser else "/panel/"
            return redirect(dest)
        phone = request.session.get(LOGIN_OTP_PHONE_KEY)
        if not phone:
            return redirect("accounts:login")
        return render(
            request,
            "accounts/phone_login.html",
            {
                "breadcrumbs": [{"title": "صفحه اصلی", "url": "/"}, {"title": "ورود", "url": None}],
                "step": "verify",
                "phone": phone,
            },
        )

    def post(self, request):
        if request.user.is_authenticated:
            dest = _default_redirect_for_user(request.user)
            return redirect(dest)
        phone = request.session.get(LOGIN_OTP_PHONE_KEY)
        if not phone:
            return redirect("accounts:login")
        code = (request.POST.get("code") or "").strip()

        if _otp_verify_is_limited(request, phone):
            return render(
                request,
                "accounts/phone_login.html",
                {
                    "breadcrumbs": [{"title": "صفحه اصلی", "url": "/"}, {"title": "ورود", "url": None}],
                    "step": "verify",
                    "phone": phone,
                    "error": "تعداد تلاش بیش از حد مجاز است. چند دقیقه بعد دوباره تلاش کنید.",
                },
            )

        user = verify_otp(phone, code)
        if user:
            del request.session[LOGIN_OTP_PHONE_KEY]
            _otp_verify_clear_failures(request, phone)
            login(request, user)
            next_url = _resolve_safe_next_url(request, user)
            return redirect(next_url)

        _otp_verify_register_failure(request, phone)
        return render(
            request,
            "accounts/phone_login.html",
            {
                "breadcrumbs": [{"title": "صفحه اصلی", "url": "/"}, {"title": "ورود", "url": None}],
                "step": "verify",
                "phone": phone,
                "error": "کد تأیید نامعتبر یا منقضی شده است.",
            },
        )


@method_decorator(ratelimit(key="ip", rate="10/m", method="POST", block=True), name="post")
class RequestOtpApiView(View):
    """API برای درخواست OTP (برای لاگین در مودال). خروجی JSON."""

    def post(self, request):
        if request.user.is_authenticated:
            return _json_login_response(True, redirect_url=_default_redirect_for_user(request.user))
        phone = (request.POST.get("phone") or "").strip()
        if not phone:
            return _json_login_response(False, "شماره موبایل را وارد کنید.")
        success, message = request_otp(phone)
        if success:
            request.session[LOGIN_OTP_PHONE_KEY] = normalize_phone(phone)
            _store_safe_next_url(request)
            return _json_login_response(True, message or "کد تأیید ارسال شد.")
        return _json_login_response(False, message or "خطا در ارسال کد.")


@method_decorator(ratelimit(key="ip", rate="20/m", method="POST", block=True), name="post")
class VerifyOtpApiView(View):
    """API برای تأیید OTP و ورود (برای مودال). خروجی JSON؛ بعد از موفقیت redirect برای رفرش صفحه."""

    def post(self, request):
        if request.user.is_authenticated:
            next_url = _resolve_safe_next_url(request, request.user)
            return _json_login_response(True, redirect_url=next_url)
        phone = request.session.get(LOGIN_OTP_PHONE_KEY)
        if not phone:
            return _json_login_response(False, "لطفاً ابتدا شماره موبایل را ارسال کنید.")
        code = (request.POST.get("code") or "").strip()
        if not code:
            return _json_login_response(False, "کد تأیید را وارد کنید.")

        if _otp_verify_is_limited(request, phone):
            return _json_login_response(False, "تعداد تلاش بیش از حد مجاز است. چند دقیقه بعد دوباره تلاش کنید.")

        user = verify_otp(phone, code)
        if user:
            del request.session[LOGIN_OTP_PHONE_KEY]
            _otp_verify_clear_failures(request, phone)
            login(request, user)
            next_url = _resolve_safe_next_url(request, user)
            return _json_login_response(True, "ورود موفق.", redirect_url=next_url)

        _otp_verify_register_failure(request, phone)
        return _json_login_response(False, "کد تأیید نامعتبر یا منقضی شده است.")


class CustomLogoutView(LogoutView):
    next_page = "/"


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {"title": "صفحه اصلی", "url": "/"},
            {"title": "ثبت نام", "url": None},
        ]
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        # superuser → admin، سایرین → پنل کاربری
        dest = "/admin/" if user.is_superuser else "/panel/"
        return redirect(dest)
