from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.urls import reverse

from apps.categories.models import Category
from apps.lead.forms import LandingLeadForm
from apps.lead.models import LandingLead
from apps.locations.models import City

from .models import ServiceProvider


def _approved_providers():
    return (
        ServiceProvider.objects.filter(
            is_active=True,
            approval_status=ServiceProvider.ApprovalStatus.APPROVED,
        )
        .prefetch_related("categories", "cities", "images")
        .order_by("name", "id")
    )


def _user_has_name_locked(user):
    if not user or not user.is_authenticated:
        return False
    return bool((getattr(user, "first_name", "") or "").strip()) and bool((getattr(user, "last_name", "") or "").strip())


def _service_lead_initial_from_user(request):
    initial = {}
    user = getattr(request, "user", None)
    if user is not None and user.is_authenticated:
        if getattr(user, "first_name", ""):
            initial["first_name"] = user.first_name
        if getattr(user, "last_name", ""):
            initial["last_name"] = user.last_name
        if getattr(user, "phone", ""):
            initial["phone"] = user.phone
        if getattr(user, "email", ""):
            initial["email"] = user.email
    return initial


def _process_service_provider_lead(request, provider):
    lock_name = _user_has_name_locked(getattr(request, "user", None))
    lock_phone = (
        getattr(request, "user", None)
        and request.user.is_authenticated
        and bool((getattr(request.user, "phone", "") or "").strip())
    )
    source_path = str(provider.id)
    redirect_url = provider.get_absolute_url()

    if request.method != "POST" or request.POST.get("service_lead") != "1":
        saved = request.session.pop("service_provider_return_form", None)
        if saved and saved.get("provider_id") == provider.id:
            initial = {
                key: saved[key]
                for key in ("first_name", "last_name", "phone", "email", "subject", "message")
                if saved.get(key)
            }
        else:
            initial = _service_lead_initial_from_user(request)
        if lock_name and request.user.is_authenticated:
            initial["first_name"] = (request.user.first_name or "").strip()
            initial["last_name"] = (request.user.last_name or "").strip()
        if lock_phone:
            initial["phone"] = (request.user.phone or "").strip()
        return None, LandingLeadForm(
            prefix="service",
            initial=initial,
            lock_name_fields=lock_name,
            lock_phone_field=lock_phone,
        )

    if not request.user.is_authenticated:
        request.session["service_provider_return_form"] = {
            "provider_id": provider.id,
            "first_name": (request.POST.get("service-first_name") or "").strip(),
            "last_name": (request.POST.get("service-last_name") or "").strip(),
            "phone": (request.POST.get("service-phone") or "").strip(),
            "email": (request.POST.get("service-email") or "").strip(),
            "subject": (request.POST.get("service-subject") or "").strip(),
            "message": (request.POST.get("service-message") or "").strip(),
        }
        if request.session["service_provider_return_form"]["phone"]:
            request.session["login_otp_phone"] = request.session["service_provider_return_form"]["phone"]
        return redirect(f"{reverse('accounts:login')}?next={redirect_url}"), LandingLeadForm(prefix="service")

    post_data = request.POST
    if lock_name or lock_phone:
        post_data = request.POST.copy()
        if lock_name:
            post_data["service-first_name"] = (request.user.first_name or "").strip()
            post_data["service-last_name"] = (request.user.last_name or "").strip()
        if lock_phone:
            post_data["service-phone"] = (request.user.phone or "").strip()

    form = LandingLeadForm(
        post_data,
        prefix="service",
        lock_name_fields=lock_name,
        lock_phone_field=lock_phone,
    )
    if form.is_valid():
        user = request.user
        first_name = (user.first_name or "").strip() if lock_name else (form.cleaned_data.get("first_name") or "").strip()
        last_name = (user.last_name or "").strip() if lock_name else (form.cleaned_data.get("last_name") or "").strip()
        phone = (user.phone or "").strip() if lock_phone else (form.cleaned_data.get("phone") or "").strip()
        email = (form.cleaned_data.get("email") or "").strip()
        subject = (form.cleaned_data.get("subject") or "").strip() or f"درخواست خدمات از {provider.name}"
        message = (form.cleaned_data.get("message") or "").strip()
        LandingLead.objects.create(
            source_type=LandingLead.SourceType.SERVICE_PROVIDER,
            source_path=source_path,
            name=f"{first_name} {last_name}".strip(),
            phone=phone,
            email=email,
            subject=subject,
            message=message,
        )

        if not lock_name:
            updated_fields = []
            if first_name and (user.first_name or "").strip() != first_name:
                user.first_name = first_name
                updated_fields.append("first_name")
            if last_name and (user.last_name or "").strip() != last_name:
                user.last_name = last_name
                updated_fields.append("last_name")
            if email and (getattr(user, "email", "") or "").strip() != email:
                user.email = email
                updated_fields.append("email")
            if updated_fields:
                user.save(update_fields=updated_fields)

        messages.success(request, "درخواست شما ثبت شد و برای ارائه‌دهنده خدمات قابل پیگیری است.")
        return redirect(redirect_url), form

    return None, form


def service_directory(request):
    categories = (
        Category.objects.filter(
            category_type=Category.CategoryType.SERVICE,
            parent__isnull=True,
            is_active=True,
        )
        .prefetch_related("images", "children")
        .order_by("sort_order", "fa_name")
    )
    providers = _approved_providers()[:12]
    breadcrumbs = [
        {"title": "صفحه اصلی", "url": "/"},
        {"title": "سرویس‌ها", "url": None},
    ]
    return render(
        request,
        "pages/service_directory.html",
        {
            "categories": categories,
            "providers": providers,
            "providers_count": _approved_providers().count(),
            "breadcrumbs": breadcrumbs,
            "seo_title": "سرویس‌های ملک | VidaHome",
            "seo_h1": "سرویس‌های ملک",
            "seo_meta_description": "دسته‌بندی سرویس‌های مرتبط با ملک و معرفی شرکت‌ها و افراد ارائه‌دهنده خدمات.",
        },
    )


def service_provider_list(request):
    providers = _approved_providers()
    q = (request.GET.get("q") or "").strip()
    category_slug = (request.GET.get("category") or "").strip()
    city_slug = (request.GET.get("city") or "").strip()
    provider_type = (request.GET.get("type") or "").strip()

    if q:
        providers = providers.filter(
            name__icontains=q,
        )
    if category_slug:
        providers = providers.filter(categories__slug=category_slug)
    if city_slug:
        providers = providers.filter(cities__slug=city_slug)
    if provider_type in dict(ServiceProvider.ProviderType.choices):
        providers = providers.filter(provider_type=provider_type)
    providers = providers.distinct()

    pagination_params = request.GET.copy()
    pagination_params.pop("page", None)
    paginator = Paginator(providers, 24)
    page_obj = paginator.get_page(request.GET.get("page", 1))
    categories = Category.objects.filter(
        category_type=Category.CategoryType.SERVICE,
        is_active=True,
    ).order_by("sort_order", "fa_name")
    cities = City.objects.filter(is_active=True).order_by("sort_order", "fa_name")
    breadcrumbs = [
        {"title": "صفحه اصلی", "url": "/"},
        {"title": "سرویس‌ها", "url": "/services/"},
        {"title": "ارائه‌دهندگان خدمات", "url": None},
    ]
    return render(
        request,
        "pages/service_provider_list.html",
        {
            "providers": page_obj.object_list,
            "page_obj": page_obj,
            "categories": categories,
            "cities": cities,
            "provider_type_choices": ServiceProvider.ProviderType.choices,
            "filter_q": q,
            "filter_category": category_slug,
            "filter_city": city_slug,
            "filter_type": provider_type,
            "pagination_query": pagination_params.urlencode(),
            "breadcrumbs": breadcrumbs,
            "seo_title": "ارائه‌دهندگان خدمات | VidaHome",
            "seo_h1": "ارائه‌دهندگان خدمات",
            "seo_meta_description": "لیست شرکت‌ها و افراد ارائه‌دهنده خدمات مرتبط با ملک در VidaHome.",
        },
    )


def service_category(request, slug):
    category = get_object_or_404(
        Category.objects.prefetch_related("images", "children"),
        slug=slug,
        category_type=Category.CategoryType.SERVICE,
        is_active=True,
    )
    child_ids = list(category.children.filter(is_active=True).values_list("id", flat=True))
    category_ids = [category.id, *child_ids]
    providers = _approved_providers().filter(categories__id__in=category_ids).distinct()
    breadcrumbs = [
        {"title": "صفحه اصلی", "url": "/"},
        {"title": "سرویس‌ها", "url": "/services/"},
        {"title": category.fa_name, "url": None},
    ]
    seo_title = category.seo_title or f"{category.fa_name} | سرویس‌ها | VidaHome"
    seo_h1 = category.seo_h1 or category.fa_name
    seo_meta = category.seo_meta_description or (category.intro_content[:160] if category.intro_content else "")
    return render(
        request,
        "pages/service_category.html",
        {
            "category": category,
            "providers": providers,
            "breadcrumbs": breadcrumbs,
            "seo_title": seo_title,
            "seo_h1": seo_h1,
            "seo_meta_description": seo_meta,
        },
    )


def service_provider_detail(request, provider_id, slug):
    provider = get_object_or_404(
        _approved_providers().select_related("owner"),
        id=provider_id,
    )
    if provider.slug != slug:
        return redirect(provider.get_absolute_url(), permanent=True)
    return _render_provider_detail(request, provider)


def service_provider_detail_by_id(request, provider_id):
    provider = get_object_or_404(
        _approved_providers().select_related("owner"),
        id=provider_id,
    )
    canonical = request.build_absolute_uri(provider.get_absolute_url())
    return _render_provider_detail(request, provider, seo_canonical=canonical)


def _render_provider_detail(request, provider, seo_canonical=None):
    redirect_resp, service_lead_form = _process_service_provider_lead(request, provider)
    if redirect_resp:
        return redirect_resp
    landing_cover = provider.get_landing_cover_image()
    category_ids = list(provider.categories.values_list("id", flat=True))
    related_providers = (
        _approved_providers()
        .filter(categories__id__in=category_ids)
        .exclude(id=provider.id)
        .distinct()[:6]
    )
    primary_category = provider.categories.first()
    breadcrumbs = [
        {"title": "صفحه اصلی", "url": "/"},
        {"title": "سرویس‌ها", "url": "/services/"},
    ]
    if primary_category:
        breadcrumbs.append({"title": primary_category.fa_name, "url": f"/services/{primary_category.slug}/"})
    breadcrumbs.append({"title": provider.name, "url": None})
    seo_title = provider.seo_title or f"{provider.name} | سرویس‌های ملک | VidaHome"
    seo_h1 = provider.seo_h1 or provider.name
    seo_meta = provider.seo_meta_description or (provider.intro_content[:160] if provider.intro_content else "")
    ctx = {
        "provider": provider,
        "landing_cover": landing_cover,
        "related_providers": related_providers,
        "breadcrumbs": breadcrumbs,
        "seo_title": seo_title,
        "seo_h1": seo_h1,
        "seo_meta_description": seo_meta,
        "service_lead_form": service_lead_form,
    }
    if seo_canonical:
        ctx["seo_canonical"] = seo_canonical
    return render(request, "pages/service_provider_detail.html", ctx)
