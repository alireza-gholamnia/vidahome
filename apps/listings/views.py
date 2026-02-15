from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic import RedirectView
from django.db.models import Q

from apps.locations.models import City, Area
from apps.categories.models import Category
from apps.seo.models import CityCategory, CityAreaCategory

from apps.blog.models import BlogPost
from apps.attributes.models import Attribute, AttributeOption, ListingAttribute

from .models import Listing


def _category_listing_filter(category):
    """فیلتر آگهی‌ها: دسته خودش + دسته‌های فرزند."""
    return Q(category=category) | Q(category__parent=category)


# =============================================================
# /s  -> لیست آگهی‌ها با فیلتر (کاتالوگ)
# =============================================================

def listing_catalog(request):
    from django.core.paginator import Paginator

    qs = (
        Listing.objects.filter(status=Listing.Status.PUBLISHED)
        .select_related("city", "area", "category")
        .prefetch_related("images")
        .order_by("-published_at", "-id")
    )

    city_slug = request.GET.get("city", "").strip()
    category_slug = request.GET.get("category", "").strip()
    area_slug = request.GET.get("area", "").strip()
    deal = request.GET.get("deal", "").strip()
    q = request.GET.get("q", "").strip()

    if city_slug:
        qs = qs.filter(city__slug=city_slug)
    if category_slug:
        qs = qs.filter(Q(category__slug=category_slug) | Q(category__parent__slug=category_slug))
    if area_slug and city_slug:
        qs = qs.filter(area__slug=area_slug, city__slug=city_slug)
    if deal in ("buy", "rent", "daily_rent", "mortgage_rent"):
        qs = qs.filter(deal=deal)
    if q:
        qs = qs.filter(
            Q(title__icontains=q)
            | Q(short_description__icontains=q)
            | Q(description__icontains=q)
        )

    # فیلترهای ویژگی (EAV)
    filterable_attrs = []
    if category_slug:
        cat = Category.objects.filter(slug=category_slug).first()
        if cat:
            cat_ids = list(
                Category.objects.filter(Q(pk=cat.pk) | Q(parent=cat)).values_list("id", flat=True)
            )
            filterable_attrs = list(
                Attribute.objects.filter(
                    is_filterable=True,
                    is_active=True,
                    categories__in=cat_ids,
                )
                .distinct()
                .order_by("sort_order", "id")
            )
    else:
        filterable_attrs = list(
            Attribute.objects.filter(is_filterable=True, is_active=True).order_by("sort_order", "id")
        )

    filter_attr_values = {}
    for key, val in request.GET.items():
        if key.startswith("attr_") and val:
            slug = key[5:]
            attr = next((a for a in filterable_attrs if a.slug == slug), None)
            if attr:
                filter_attr_values[attr.slug] = val

    for attr in filterable_attrs:
        val = filter_attr_values.get(attr.slug)
        if not val:
            continue
        if attr.value_type == Attribute.ValueType.INTEGER:
            try:
                v = int(val)
                qs = qs.filter(attribute_values__attribute=attr, attribute_values__value_int=v)
            except ValueError:
                pass
        elif attr.value_type == Attribute.ValueType.BOOLEAN:
            qs = qs.filter(
                attribute_values__attribute=attr,
                attribute_values__value_bool=(val == "1"),
            )
        elif attr.value_type == Attribute.ValueType.CHOICE:
            try:
                opt_id = int(val)
                qs = qs.filter(
                    attribute_values__attribute=attr,
                    attribute_values__value_option_id=opt_id,
                )
            except ValueError:
                pass
        elif attr.value_type == Attribute.ValueType.STRING:
            qs = qs.filter(
                attribute_values__attribute=attr,
                attribute_values__value_str=val,
            )
    if filter_attr_values:
        qs = qs.distinct()

    paginator = Paginator(qs, 24)
    page = request.GET.get("page", 1)
    try:
        page_num = int(page)
        if page_num < 1:
            page_num = 1
    except ValueError:
        page_num = 1
    listings = paginator.get_page(page_num)

    cities = City.objects.filter(is_active=True).order_by("sort_order", "fa_name")
    categories = Category.objects.filter(parent__isnull=True, is_active=True).order_by("sort_order", "fa_name")
    areas = []
    if city_slug:
        city = City.objects.filter(slug=city_slug, is_active=True).first()
        if city:
            areas = Area.objects.filter(city=city, is_active=True).order_by("sort_order", "fa_name")

    breadcrumbs = [
        {"title": "صفحه اصلی", "url": "/"},
        {"title": "آگهی‌های املاک", "url": None},
    ]
    title = "آگهی‌های املاک"
    if city_slug and (c := City.objects.filter(slug=city_slug).first()):
        title = f"آگهی‌های {c.fa_name}"

    # گزینه‌های فیلتر ویژگی‌ها
    attr_filters = []
    for attr in filterable_attrs:
        options = [("", "همه")]
        if attr.value_type == Attribute.ValueType.INTEGER:
            opts = AttributeOption.objects.filter(attribute=attr).order_by("sort_order", "id")
            options.extend((str(opt.value), opt.value) for opt in opts)
        elif attr.value_type == Attribute.ValueType.BOOLEAN:
            options.extend([("1", "بله"), ("0", "خیر")])
        elif attr.value_type == Attribute.ValueType.CHOICE:
            opts = AttributeOption.objects.filter(attribute=attr).order_by("sort_order", "id")
            options.extend((str(opt.id), opt.value) for opt in opts)
        current = filter_attr_values.get(attr.slug, "")
        attr_filters.append({"attr": attr, "options": options, "current": current})

    # Query string for pagination (exclude page)
    from urllib.parse import urlencode
    params = dict(request.GET)
    params.pop("page", None)
    pagination_query = urlencode(params, doseq=True)

    return render(
        request,
        "pages/listing_catalog.html",
        {
            "listings": listings,
            "cities": cities,
            "categories": categories,
            "areas": areas,
            "attr_filters": attr_filters,
            "breadcrumbs": breadcrumbs,
            "seo_h1": title,
            "seo_title": f"{title} | VidaHome",
            "seo_meta_description": "جستجو و مشاهده آگهی‌های خرید، فروش و اجاره املاک در VidaHome",
            "filter_city": city_slug,
            "filter_category": category_slug,
            "filter_area": area_slug,
            "filter_deal": deal,
            "filter_q": q,
            "pagination_query": pagination_query,
        },
    )




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
    city = City.objects.filter(slug=slug, is_active=True).prefetch_related("images").first()
    if city:
        areas = Area.objects.filter(city=city, is_active=True).order_by("sort_order", "id")
        listings = (
            Listing.objects.filter(city=city, status=Listing.Status.PUBLISHED)
            .select_related("category", "area")
            .prefetch_related("images")
            .order_by("-published_at", "-id")[:24]
        )
        seo = _build_seo_for_city(request, city)
        breadcrumbs = [
            {"title": "صفحه اصلی", "url": "/"},
            {"title": "شهرها", "url": "/cities/"},
            {"title": city.fa_name, "url": None},
        ]
        city_posts = (
            BlogPost.objects.filter(city=city, status=BlogPost.Status.PUBLISHED)
            .select_related("blog_category", "author")
            .order_by("-published_at", "-id")[:6]
        )
        return render(
            request,
            "pages/city_landing.html",
            {
                "city": city,
                "areas": areas,
                "listings": listings,
                "city_posts": city_posts,
                "breadcrumbs": breadcrumbs,
                **seo,
            },
        )

    category = Category.objects.filter(slug=slug, is_active=True).prefetch_related("images").first()
    if category:
        listings = (
            Listing.objects.filter(_category_listing_filter(category), status=Listing.Status.PUBLISHED)
            .select_related("city", "area", "category")
            .prefetch_related("images")
            .order_by("-published_at", "-id")[:24]
        )
        children = Category.objects.filter(parent=category, is_active=True).order_by("sort_order", "id")
        seo = _build_seo_for_category(request, category)
        breadcrumbs = [
            {"title": "صفحه اصلی", "url": "/"},
            {"title": "دسته‌بندی‌ها", "url": "/categories/"},
            {"title": category.fa_name, "url": None},
        ]
        category_posts = (
            BlogPost.objects.filter(
                Q(listing_category=category) | Q(listing_category__parent=category),
                status=BlogPost.Status.PUBLISHED,
            )
            .select_related("blog_category", "author")
            .order_by("-published_at", "-id")[:6]
        )
        return render(
            request,
            "pages/category_landing.html",
            {
                "category": category,
                "listings": listings,
                "children": children,
                "category_posts": category_posts,
                "breadcrumbs": breadcrumbs,
                **seo,
            },
        )

    raise Http404()


# =============================================================
# /s/{city}/{category} OR /s/{city}/{area}
# =============================================================

def city_context(request, city_slug, context_slug):
    city = get_object_or_404(City, slug=city_slug, is_active=True)

    area = Area.objects.filter(city=city, slug=context_slug, is_active=True).prefetch_related("images").first()
    if area:
        listings = (
            Listing.objects.filter(city=city, area=area, status=Listing.Status.PUBLISHED)
            .select_related("category", "area")
            .prefetch_related("images")
            .order_by("-published_at", "-id")[:24]
        )
        seo = _build_seo_for_area(request, area)
        breadcrumbs = [
            {"title": "صفحه اصلی", "url": "/"},
            {"title": "شهرها", "url": "/cities/"},
            {"title": city.fa_name, "url": f"/s/{city.slug}/"},
            {"title": area.fa_name, "url": None},
        ]
        return render(
            request,
            "pages/area_landing.html",
            {"city": city, "area": area, "listings": listings, "breadcrumbs": breadcrumbs, **seo},
        )

    category = Category.objects.filter(slug=context_slug, is_active=True).prefetch_related("images").first()
    if category:
        landing = CityCategory.objects.filter(city=city, category=category, is_active=True).prefetch_related("images").first()

        listings = (
            Listing.objects.filter(city=city, status=Listing.Status.PUBLISHED)
            .filter(_category_listing_filter(category))
            .select_related("area", "category")
            .prefetch_related("images")
            .order_by("-published_at", "-id")[:24]
        )
        breadcrumbs = [
            {"title": "صفحه اصلی", "url": "/"},
            {"title": "شهرها", "url": "/cities/"},
            {"title": city.fa_name, "url": f"/s/{city.slug}/"},
            {"title": category.fa_name, "url": None},
        ]
        if landing:
            seo = _build_seo_for_landing(
                request,
                landing,
                default_title=f"{category.fa_name} در {city.fa_name} | VidaHome",
                default_h1=f"{category.fa_name} در {city.fa_name}",
                default_desc=f"آگهی‌های {category.fa_name} در {city.fa_name}. خرید، فروش، رهن و اجاره با VidaHome.",
            )
            landing_cover = landing.get_landing_cover_image()
            return render(
                request,
                "pages/city_category_landing.html",
                {"city": city, "category": category, "landing": landing, "landing_cover": landing_cover, "listings": listings, "breadcrumbs": breadcrumbs, **seo},
            )

        landing_cover = category.get_landing_cover_image()
        seo = {
            "seo_title": f"{category.fa_name} در {city.fa_name} | VidaHome",
            "seo_meta_description": f"آگهی‌های {category.fa_name} در {city.fa_name}. خرید، فروش، رهن و اجاره با VidaHome.",
            "seo_h1": f"{category.fa_name} در {city.fa_name}",
            "seo_canonical": request.build_absolute_uri(),
            "seo_robots": "index, follow",
            "intro_content": "",
            "main_content": "",
        }
        return render(
            request,
            "pages/city_category_landing.html",
            {"city": city, "category": category, "landing_cover": landing_cover, "listings": listings, "breadcrumbs": breadcrumbs, **seo},
        )

    raise Http404()


# =============================================================
# /s/{city}/{area}/{category}
# =============================================================

def area_category(request, city_slug, area_slug, category_slug):
    city = get_object_or_404(City, slug=city_slug, is_active=True)
    area = get_object_or_404(Area, city=city, slug=area_slug, is_active=True)
    category = get_object_or_404(Category.objects.prefetch_related("images"), slug=category_slug, is_active=True)

    landing = CityAreaCategory.objects.filter(
        city=city,
        area=area,
        category=category,
        is_active=True
    ).prefetch_related("images").first()

    listings = (
        Listing.objects.filter(city=city, area=area, status=Listing.Status.PUBLISHED)
        .filter(_category_listing_filter(category))
        .select_related("category", "area")
        .prefetch_related("images")
        .order_by("-published_at", "-id")[:24]
    )
    breadcrumbs = [
        {"title": "صفحه اصلی", "url": "/"},
        {"title": "شهرها", "url": "/cities/"},
        {"title": city.fa_name, "url": f"/s/{city.slug}/"},
        {"title": area.fa_name, "url": f"/s/{city.slug}/{area.slug}/"},
        {"title": category.fa_name, "url": None},
    ]
    if landing:
        seo = _build_seo_for_landing(
            request,
            landing,
            default_title=f"{category.fa_name} در {area.fa_name} {city.fa_name} | VidaHome",
            default_h1=f"{category.fa_name} در {area.fa_name}",
            default_desc=f"آگهی‌های {category.fa_name} در {area.fa_name} {city.fa_name}. خرید، فروش، رهن و اجاره با VidaHome.",
        )
        landing_cover = landing.get_landing_cover_image()
        return render(
            request,
            "pages/area_category_landing.html",
            {"city": city, "area": area, "category": category, "landing": landing, "landing_cover": landing_cover, "listings": listings, "breadcrumbs": breadcrumbs, **seo},
        )

    landing_cover = category.get_landing_cover_image()
    seo = {
        "seo_title": f"{category.fa_name} در {area.fa_name} {city.fa_name} | VidaHome",
        "seo_meta_description": f"آگهی‌های {category.fa_name} در {area.fa_name} {city.fa_name}. خرید، فروش، رهن و اجاره با VidaHome.",
        "seo_h1": f"{category.fa_name} در {area.fa_name}",
        "seo_canonical": request.build_absolute_uri(),
        "seo_robots": "index, follow",
        "intro_content": "",
        "main_content": "",
    }
    return render(
        request,
        "pages/area_category_landing.html",
        {"city": city, "area": area, "category": category, "landing_cover": landing_cover, "listings": listings, "breadcrumbs": breadcrumbs, **seo},
    )


# =============================================================
# /l/{id}-{slug}  -> Listing Detail
# =============================================================

def _listing_breadcrumbs(listing: Listing):
    breadcrumbs = [
        {"title": "صفحه اصلی", "url": "/"},
        {"title": "شهرها", "url": "/cities/"},
        {"title": listing.city.fa_name, "url": listing.city.get_absolute_url()},
    ]
    if listing.area:
        breadcrumbs.append({"title": listing.area.fa_name, "url": listing.area.get_absolute_url()})
    breadcrumbs.append({"title": listing.title, "url": None})
    return breadcrumbs


def listing_detail(request, listing_id: int, slug: str):
    listing = (
        Listing.objects
        .select_related("city", "area", "category", "agency")
        .prefetch_related("images", "attribute_values__attribute", "attribute_values__value_option")
        .filter(id=listing_id, status=Listing.Status.PUBLISHED)
        .first()
    )

    if not listing:
        raise Http404()

    seo = _build_seo_for_listing(request, listing)
    breadcrumbs = _listing_breadcrumbs(listing)
    return render(request, "pages/listing_detail.html", {"listing": listing, "breadcrumbs": breadcrumbs, **seo})

def listing_detail_by_id(request, listing_id: int):
    listing = (
        Listing.objects
        .select_related("city", "area", "category", "agency")
        .prefetch_related("images", "attribute_values__attribute", "attribute_values__value_option")
        .filter(id=listing_id, status=Listing.Status.PUBLISHED)
        .first()
    )
    if not listing:
        raise Http404()

    seo = _build_seo_for_listing(request, listing)
    seo["seo_canonical"] = request.build_absolute_uri(listing.get_absolute_url())
    breadcrumbs = _listing_breadcrumbs(listing)
    return render(request, "pages/listing_detail.html", {"listing": listing, "breadcrumbs": breadcrumbs, **seo})
