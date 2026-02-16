from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from .forms import SignUpForm
from .models import User
from .services import request_otp, verify_otp

LOGIN_OTP_PHONE_KEY = "login_otp_phone"


class PhoneLoginView(View):
    """ورود با موبایل - مرحله ۱: دریافت شماره و ارسال OTP"""

    def get(self, request):
        if request.user.is_authenticated:
            dest = "/admin/" if request.user.is_superuser else "/panel/"
            return redirect(dest)
        return render(
            request,
            "accounts/phone_login.html",
            {
                "breadcrumbs": [{"title": "صفحه اصلی", "url": "/"}, {"title": "ورود", "url": None}],
                "step": "phone",
            },
        )

    def post(self, request):
        if request.user.is_authenticated:
            dest = "/admin/" if request.user.is_superuser else "/panel/"
            return redirect(dest)
        phone = (request.POST.get("phone") or "").strip()
        success, message = request_otp(phone)
        if success:
            request.session[LOGIN_OTP_PHONE_KEY] = phone
            next_url = request.GET.get("next") or request.POST.get("next")
            if next_url:
                request.session["login_next_url"] = next_url
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
            dest = "/admin/" if request.user.is_superuser else "/panel/"
            return redirect(dest)
        phone = request.session.get(LOGIN_OTP_PHONE_KEY)
        if not phone:
            return redirect("accounts:login")
        code = (request.POST.get("code") or "").strip()
        user = verify_otp(phone, code)
        if user:
            del request.session[LOGIN_OTP_PHONE_KEY]
            login(request, user)
            next_url = (
                request.GET.get("next")
                or request.POST.get("next")
                or request.session.pop("login_next_url", None)
            )
            if not next_url or next_url == "/":
                next_url = "/admin/" if user.is_superuser else "/panel/"
            return redirect(next_url)
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
