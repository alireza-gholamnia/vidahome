from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic import RedirectView

from apps.locations.models import City, Area
from apps.categories.models import Category
from apps.seo.models import CityCategory, CityAreaCategory

from .models import Listing


# =============================================================
# /s  -> redirect
# =============================================================
s_root_redirect = RedirectView.as_view(url="/", permanent=False)


# =============================================================
# SEO helpers
# =============================================================

def _build_seo_for_city(request, city: City):
    is_noindex = (not city.allow_index) or city.seo_noindex

    default_title = f"{city.fa_name} | VidaHome"
    default_h1 = f"شهر {city.fa_name}"
    default_desc = (city.seo_meta_description or "").strip()

    canonical = city.seo_canonical or request.build_absolute_uri()

    return {
        "seo_title": (city.seo_title or default_title).strip(),
        "seo_meta_description": default_desc,
        "seo_h1": (city.seo_h1 or default_h1).strip(),
        "seo_canonical": canonical.strip(),
        "seo_robots": "noindex, follow" if is_noindex else "index, follow",
        "intro_content": (city.intro_content or "").strip(),
        "main_content": city.main_content or "",
    }


def _build_seo_for_category(request, category: Category):
    is_noindex = (not category.allow_index) or category.seo_noindex

    default_title = f"{category.fa_name} | VidaHome"
    default_h1 = category.fa_name
    default_desc = (category.seo_meta_description or "").strip()

    canonical = category.seo_canonical or request.build_absolute_uri()

    return {
        "seo_title": (category.seo_title or default_title).strip(),
        "seo_meta_description": default_desc,
        "seo_h1": (category.seo_h1 or default_h1).strip(),
        "seo_canonical": canonical.strip(),
        "seo_robots": "noindex, follow" if is_noindex else "index, follow",
        "intro_content": (category.intro_content or "").strip(),
        "main_content": category.main_content or "",
    }


def _build_seo_for_area(request, area: Area):
    is_noindex = (not area.allow_index) or area.seo_noindex

    default_title = f"محله {area.fa_name} در {area.city.fa_name} | VidaHome"
    default_h1 = f"محله {area.fa_name}"
    default_desc = f"آگهی‌ها و فایل‌های ملکی در {area.fa_name} {area.city.fa_name}. خرید، فروش، رهن و اجاره در VidaHome."

    canonical = area.seo_canonical or request.build_absolute_uri()

    return {
        "seo_title": (area.seo_title or default_title).strip(),
        "seo_meta_description": (area.seo_meta_description or default_desc).strip(),
        "seo_h1": (area.seo_h1 or default_h1).strip(),
        "seo_canonical": canonical.strip(),
        "seo_robots": "noindex, follow" if is_noindex else "index, follow",
        "intro_content": (area.intro_content or "").strip(),
        "main_content": area.main_content or "",
    }


def _build_seo_for_landing(request, landing, *, default_title: str, default_h1: str, default_desc: str):
    is_noindex = (not landing.allow_index) or landing.seo_noindex
    canonical = landing.seo_canonical or request.build_absolute_uri()

    return {
        "seo_title": (landing.seo_title or default_title).strip(),
        "seo_meta_description": (landing.seo_meta_description or default_desc).strip(),
        "seo_h1": (landing.seo_h1 or default_h1).strip(),
        "seo_canonical": canonical.strip(),
        "seo_robots": "noindex, follow" if is_noindex else "index, follow",
        "intro_content": (landing.intro_content or "").strip(),
        "main_content": landing.main_content or "",
    }


def _build_seo_for_listing(request, listing: Listing):
    is_noindex = (not listing.allow_index) or listing.seo_noindex

    default_title = f"{listing.title} | VidaHome"
    default_h1 = listing.title

    if listing.short_description:
        default_desc = listing.short_description.strip()
    else:
        default_desc = f"جزئیات آگهی {listing.title} در {listing.city.fa_name}."

    canonical_default = request.build_absolute_uri(listing.get_absolute_url())
    canonical = (listing.seo_canonical or canonical_default).strip()

    return {
        "seo_title": (listing.seo_title or default_title).strip(),
        "seo_meta_description": (listing.seo_meta_description or default_desc).strip(),
        "seo_h1": (listing.seo_h1 or default_h1).strip(),
        "seo_canonical": canonical,
        "seo_robots": "noindex, follow" if is_noindex else "index, follow",
        "intro_content": "",
        "main_content": "",
    }


# =============================================================
# /s/{slug}  -> City OR Category
# =============================================================

def s_one_segment(request, slug):
    city = City.objects.filter(slug=slug, is_active=True).first()
    if city:
        areas = Area.objects.filter(city=city, is_active=True).order_by("sort_order", "id")
        seo = _build_seo_for_city(request, city)
        return render(request, "pages/city_landing.html", {"city": city, "areas": areas, **seo})

    category = Category.objects.filter(slug=slug, is_active=True).first()
    if category:
        seo = _build_seo_for_category(request, category)
        return render(request, "pages/category_landing.html", {"category": category, **seo})

    raise Http404()


# =============================================================
# /s/{city}/{category} OR /s/{city}/{area}
# =============================================================

def city_context(request, city_slug, context_slug):
    city = get_object_or_404(City, slug=city_slug, is_active=True)

    area = Area.objects.filter(city=city, slug=context_slug, is_active=True).first()
    if area:
        seo = _build_seo_for_area(request, area)
        return render(request, "pages/area_landing.html", {"city": city, "area": area, **seo})

    category = Category.objects.filter(slug=context_slug, is_active=True).first()
    if category:
        landing = CityCategory.objects.filter(city=city, category=category, is_active=True).first()

        if landing:
            seo = _build_seo_for_landing(
                request,
                landing,
                default_title=f"{category.fa_name} در {city.fa_name} | VidaHome",
                default_h1=f"{category.fa_name} در {city.fa_name}",
                default_desc=f"آگهی‌های {category.fa_name} در {city.fa_name}. خرید، فروش، رهن و اجاره با VidaHome.",
            )
            return render(
                request,
                "pages/city_category_landing.html",
                {"city": city, "category": category, "landing": landing, **seo},
            )

        seo = {
            "seo_title": f"{category.fa_name} در {city.fa_name} | VidaHome",
            "seo_meta_description": f"آگهی‌های {category.fa_name} در {city.fa_name}. خرید، فروش، رهن و اجاره با VidaHome.",
            "seo_h1": f"{category.fa_name} در {city.fa_name}",
            "seo_canonical": request.build_absolute_uri(),
            "seo_robots": "index, follow",
            "intro_content": "",
            "main_content": "",
        }
        return render(request, "pages/city_category_landing.html", {"city": city, "category": category, **seo})

    raise Http404()


# =============================================================
# /s/{city}/{area}/{category}
# =============================================================

def area_category(request, city_slug, area_slug, category_slug):
    city = get_object_or_404(City, slug=city_slug, is_active=True)
    area = get_object_or_404(Area, city=city, slug=area_slug, is_active=True)
    category = get_object_or_404(Category, slug=category_slug, is_active=True)

    landing = CityAreaCategory.objects.filter(
        city=city,
        area=area,
        category=category,
        is_active=True
    ).first()

    if landing:
        seo = _build_seo_for_landing(
            request,
            landing,
            default_title=f"{category.fa_name} در {area.fa_name} {city.fa_name} | VidaHome",
            default_h1=f"{category.fa_name} در {area.fa_name}",
            default_desc=f"آگهی‌های {category.fa_name} در {area.fa_name} {city.fa_name}. خرید، فروش، رهن و اجاره با VidaHome.",
        )
        return render(
            request,
            "pages/area_category_landing.html",
            {"city": city, "area": area, "category": category, "landing": landing, **seo},
        )

    seo = {
        "seo_title": f"{category.fa_name} در {area.fa_name} {city.fa_name} | VidaHome",
        "seo_meta_description": f"آگهی‌های {category.fa_name} در {area.fa_name} {city.fa_name}. خرید، فروش، رهن و اجاره با VidaHome.",
        "seo_h1": f"{category.fa_name} در {area.fa_name}",
        "seo_canonical": request.build_absolute_uri(),
        "seo_robots": "index, follow",
        "intro_content": "",
        "main_content": "",
    }
    return render(request, "pages/area_category_landing.html", {"city": city, "area": area, "category": category, **seo})


# =============================================================
# /l/{id}-{slug}  -> Listing Detail
# =============================================================

def listing_detail(request, listing_id: int, slug: str):
    listing = (
        Listing.objects
        .select_related("city", "area", "category")
        .filter(id=listing_id, status=Listing.Status.PUBLISHED)
        .first()
    )
    if not listing:
        raise Http404()

    seo = _build_seo_for_listing(request, listing)
    return render(request, "pages/listing_detail.html", {"listing": listing, **seo})

def listing_detail_by_id(request, listing_id: int):
    listing = (
        Listing.objects
        .select_related("city", "area", "category")
        .filter(id=listing_id, status=Listing.Status.PUBLISHED)
        .first()
    )
    if not listing:
        raise Http404()

    seo = _build_seo_for_listing(request, listing)
    # نکته: canonical اینجا هم باید canonical استاندارد باشه
    seo["seo_canonical"] = request.build_absolute_uri(listing.get_absolute_url())

    return render(request, "pages/listing_detail.html", {"listing": listing, **seo})
