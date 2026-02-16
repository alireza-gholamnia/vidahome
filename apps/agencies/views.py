from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q

from .models import Agency
from apps.accounts.models import User
from apps.listings.models import Listing


def _render_agency_landing(request, agency, seo_canonical=None):
    listings = (
        Listing.objects.filter(agency=agency, status=Listing.Status.PUBLISHED)
        .select_related("city", "area", "category")
        .prefetch_related("images")
        .order_by("-published_at", "-id")[:24]
    )
    employees = agency.employees.filter(is_active=True).select_related("agency")
    landing_cover = agency.get_landing_cover_image()
    seo_title = agency.seo_title or f"{agency.name} | VidaHome"
    seo_h1 = agency.seo_h1 or agency.name
    seo_meta = agency.seo_meta_description or (agency.intro_content[:160] if agency.intro_content else "")
    breadcrumbs = [
        {"title": "صفحه اصلی", "url": "/"},
        {"title": "مشاوره‌های املاک", "url": "/agencies/"},
        {"title": agency.name, "url": None},
    ]
    ctx = {
        "agency": agency,
        "listings": listings,
        "employees": employees,
        "landing_cover": landing_cover,
        "seo_title": seo_title,
        "seo_h1": seo_h1,
        "seo_meta_description": seo_meta,
        "breadcrumbs": breadcrumbs,
    }
    if seo_canonical:
        ctx["seo_canonical"] = seo_canonical
    return render(request, "pages/agency_landing.html", ctx)


def agency_list(request):
    from apps.locations.models import City

    agencies = Agency.objects.filter(
        is_active=True, approval_status=Agency.ApprovalStatus.APPROVED
    ).prefetch_related("cities", "images").order_by("name")
    city_slug = request.GET.get("city", "").strip()
    if city_slug:
        agencies = agencies.filter(cities__slug=city_slug).distinct()
    cities = City.objects.filter(is_active=True).order_by("sort_order", "fa_name")
    breadcrumbs = [
        {"title": "صفحه اصلی", "url": "/"},
        {"title": "مشاوره‌های املاک", "url": None},
    ]
    return render(
        request,
        "pages/agency_list.html",
        {
            "agencies": agencies,
            "breadcrumbs": breadcrumbs,
            "cities": cities,
            "filter_city": city_slug,
        },
    )


def agency_landing(request, agency_id, slug):
    agency = get_object_or_404(
        Agency.objects.select_related("owner", "owner__agency").prefetch_related("images", "cities", "employees", "owner__owned_agencies"),
        id=agency_id,
        is_active=True,
        approval_status=Agency.ApprovalStatus.APPROVED,
    )
    return _render_agency_landing(request, agency)


def agency_landing_by_id(request, agency_id):
    agency = get_object_or_404(
        Agency.objects.select_related("owner", "owner__agency").prefetch_related("images", "cities", "employees", "owner__owned_agencies"),
        id=agency_id,
        is_active=True,
        approval_status=Agency.ApprovalStatus.APPROVED,
    )
    canonical = request.build_absolute_uri(agency.get_absolute_url())
    return _render_agency_landing(request, agency, seo_canonical=canonical)


def agency_landing_by_slug(request, slug):
    agency = get_object_or_404(
        Agency.objects.filter(
            is_active=True, approval_status=Agency.ApprovalStatus.APPROVED
        ),
        slug=slug,
    )
    return redirect(agency.get_absolute_url(), permanent=True)


def _get_agent_listings(user):
    """آگهی‌های منتشرشده مرتبط با مشاور (صاحب یا کارمند)."""
    qs = Listing.objects.filter(
        status=Listing.Status.PUBLISHED
    ).select_related("city", "area", "category").prefetch_related("images")
    # صاحب: آگهی‌های مشاوره‌هایش یا ایجادشده توسط خودش
    owned = Agency.objects.filter(
        owner=user, is_active=True, approval_status=Agency.ApprovalStatus.APPROVED
    ).values_list("id", flat=True)
    return qs.filter(
        Q(agency_id__in=owned) | Q(created_by=user) | Q(agency=user.agency)
    ).order_by("-published_at", "-id")[:24]


def agent_landing(request, user_id, slug=None):
    """لندینگ مشاور — صاحب یا کارمند مشاوره املاک."""
    agent = get_object_or_404(
        User.objects.select_related("agency").prefetch_related("owned_agencies", "groups"),
        pk=user_id,
        is_active=True,
    )
    if not agent.is_agent():
        raise Http404()
    # تطبیق اسلاگ در URL — اگر کاربر اسلاگ دارد و اسلاگ URL متفاوت است، ریدایرکت
    if agent.slug and slug != agent.slug:
        return redirect(agent.get_absolute_url(), permanent=True)
    agencies = list(
        agent.owned_agencies.filter(
            is_active=True, approval_status=Agency.ApprovalStatus.APPROVED
        )
    )
    if agent.agency_id and agent.agency.is_active and agent.agency.approval_status == Agency.ApprovalStatus.APPROVED:
        if agent.agency not in agencies:
            agencies.append(agent.agency)
    listings = _get_agent_listings(agent)
    display_name = agent.get_full_name() or agent.username or f"کاربر {agent.id}"
    seo_title = f"{display_name} | مشاور املاک | VidaHome"
    seo_h1 = display_name
    seo_meta = f"صفحه مشاور املاک {display_name} — آگهی‌ها و اطلاعات تماس."
    breadcrumbs = [
        {"title": "صفحه اصلی", "url": "/"},
        {"title": "مشاورین املاک", "url": "/agencies/"},
        {"title": display_name, "url": None},
    ]
    canonical = request.build_absolute_uri(agent.get_absolute_url())
    return render(
        request,
        "pages/agent_landing.html",
        {
            "agent": agent,
            "agencies": agencies,
            "listings": listings,
            "display_name": display_name,
            "seo_title": seo_title,
            "seo_h1": seo_h1,
            "seo_meta_description": seo_meta,
            "breadcrumbs": breadcrumbs,
            "seo_canonical": canonical,
        },
    )


def agent_landing_by_id(request, user_id):
    """لندینگ مشاور فقط با ID — برای canonical."""
    agent = get_object_or_404(
        User.objects.select_related("agency").prefetch_related("owned_agencies"),
        pk=user_id,
        is_active=True,
    )
    if not agent.is_agent():
        raise Http404()
    canonical = request.build_absolute_uri(agent.get_absolute_url())
    listings = _get_agent_listings(agent)
    agencies = list(
        agent.owned_agencies.filter(
            is_active=True, approval_status=Agency.ApprovalStatus.APPROVED
        )
    )
    if agent.agency_id and agent.agency.is_active and agent.agency.approval_status == Agency.ApprovalStatus.APPROVED:
        if agent.agency not in agencies:
            agencies.append(agent.agency)
    display_name = agent.get_full_name() or agent.username or f"کاربر {agent.id}"
    return render(
        request,
        "pages/agent_landing.html",
        {
            "agent": agent,
            "agencies": agencies,
            "listings": listings,
            "display_name": display_name,
            "seo_title": f"{display_name} | مشاور املاک | VidaHome",
            "seo_h1": display_name,
            "seo_meta_description": f"صفحه مشاور املاک {display_name} — آگهی‌ها و اطلاعات تماس.",
            "breadcrumbs": [
                {"title": "صفحه اصلی", "url": "/"},
                {"title": "مشاورین املاک", "url": "/agencies/"},
                {"title": display_name, "url": None},
            ],
            "seo_canonical": canonical,
        },
    )
