from django.shortcuts import redirect, render, get_object_or_404
from .models import Agency
from apps.listings.models import Listing


def _render_agency_landing(request, agency, seo_canonical=None):
    listings = (
        Listing.objects.filter(agency=agency, status=Listing.Status.PUBLISHED)
        .select_related("city", "area", "category")
        .prefetch_related("images")
        .order_by("-published_at", "-id")[:24]
    )
    employees = agency.employees.filter(is_active=True)
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

    agencies = Agency.objects.filter(is_active=True).prefetch_related("cities", "images").order_by("name")
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
        Agency.objects.prefetch_related("images", "cities", "employees"),
        id=agency_id,
        is_active=True,
    )
    return _render_agency_landing(request, agency)


def agency_landing_by_id(request, agency_id):
    agency = get_object_or_404(
        Agency.objects.prefetch_related("images", "cities", "employees"),
        id=agency_id,
        is_active=True,
    )
    canonical = request.build_absolute_uri(agency.get_absolute_url())
    return _render_agency_landing(request, agency, seo_canonical=canonical)


def agency_landing_by_slug(request, slug):
    agency = get_object_or_404(
        Agency.objects.filter(is_active=True),
        slug=slug,
    )
    return redirect(agency.get_absolute_url(), permanent=True)
