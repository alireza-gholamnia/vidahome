from django.shortcuts import render, get_object_or_404
from .models import Agency
from apps.listings.models import Listing


def agency_landing(request, slug):
    agency = get_object_or_404(
        Agency.objects.prefetch_related("images", "cities", "employees"),
        slug=slug,
        is_active=True,
    )
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
        {"title": "مشاوره‌های املاک", "url": None},
        {"title": agency.name, "url": None},
    ]
    return render(
        request,
        "pages/agency_landing.html",
        {
            "agency": agency,
            "listings": listings,
            "employees": employees,
            "landing_cover": landing_cover,
            "seo_title": seo_title,
            "seo_h1": seo_h1,
            "seo_meta_description": seo_meta,
            "breadcrumbs": breadcrumbs,
        },
    )
