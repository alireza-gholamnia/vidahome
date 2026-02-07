from django.shortcuts import render, get_object_or_404
from django.http import Http404

from apps.locations.models import City, Area
from apps.categories.models import Category


# =============================================================
# /s/{category}
# =============================================================
def category_landing(request, category_slug):
    """
    URL: /s/{category}
    Example: /s/apartment

    Category-only landing page (no city context)
    """
    category = get_object_or_404(Category, slug=category_slug, is_active=True)
    return render(request, "pages/category_landing.html", {"category": category})


# =============================================================
# /s/{city}
# =============================================================
def city_landing(request, city_slug):
    """
    URL: /s/{city}
    Example: /s/rasht

    City landing page + list of active areas
    """
    city = get_object_or_404(City, slug=city_slug, is_active=True)

    areas = (
        Area.objects
        .filter(city=city, is_active=True)
        .order_by("sort_order", "id")
    )

    return render(
        request,
        "pages/city_landing.html",
        {"city": city, "areas": areas},
    )


# =============================================================
# /s/{city}/{category}
# /s/{city}/{area}
# =============================================================
def city_context(request, city_slug, context_slug):
    """
    URL:
      /s/{city}/{category}
      /s/{city}/{area}

    Examples:
      /s/rasht/apartment  → City + Category landing
      /s/rasht/golsar    → City + Area landing

    Resolution order:
      1) Area (scoped to city)  [more specific]
      2) Category (global)
    """
    city = get_object_or_404(City, slug=city_slug, is_active=True)

    # 1️⃣ Try as Area under this city
    area = Area.objects.filter(
        city=city,
        slug=context_slug,
        is_active=True,
    ).first()

    if area:
        # /s/{city}/{area}
        return render(
            request,
            "pages/area_landing.html",
            {"city": city, "area": area},
        )

    # 2️⃣ Try as Category
    category = Category.objects.filter(
        slug=context_slug,
        is_active=True,
    ).first()

    if category:
        # /s/{city}/{category}
        return render(
            request,
            "pages/city_category_landing.html",
            {"city": city, "category": category},
        )

    raise Http404()


# =============================================================
# /s/{city}/{area}/{category}
# =============================================================
def area_category(request, city_slug, area_slug, category_slug):
    """
    URL: /s/{city}/{area}/{category}
    Example: /s/rasht/golsar/apartment
    """
    city = get_object_or_404(City, slug=city_slug, is_active=True)
    area = get_object_or_404(Area, city=city, slug=area_slug, is_active=True)
    category = get_object_or_404(Category, slug=category_slug, is_active=True)

    return render(
        request,
        "pages/area_category_landing.html",
        {"city": city, "area": area, "category": category},
    )
