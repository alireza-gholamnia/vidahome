from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic import RedirectView

from apps.locations.models import City, Area
from apps.categories.models import Category


# =============================================================
# /s  -> redirect
# =============================================================
s_root_redirect = RedirectView.as_view(url="/", permanent=False)


# =============================================================
# /s/{slug}  -> City OR Category
# =============================================================
def s_one_segment(request, slug):
    """
    URL: /s/{slug}

    - If slug matches City.slug -> City landing
    - Else if slug matches Category.slug -> Category landing
    - Else 404
    """
    city = City.objects.filter(slug=slug, is_active=True).first()
    if city:
        areas = Area.objects.filter(city=city, is_active=True).order_by("sort_order", "id")
        return render(request, "pages/city_landing.html", {"city": city, "areas": areas})

    category = Category.objects.filter(slug=slug, is_active=True).first()
    if category:
        return render(request, "pages/category_landing.html", {"category": category})

    raise Http404()


# =============================================================
# /s/{city}/{category} OR /s/{city}/{area}
# =============================================================
def city_context(request, city_slug, context_slug):
    """
    URL:
      /s/{city}/{category}
      /s/{city}/{area}

    Priority:
      1) Area (scoped to city)
      2) Category (global)
    """
    city = get_object_or_404(City, slug=city_slug, is_active=True)

    area = Area.objects.filter(city=city, slug=context_slug, is_active=True).first()
    if area:
        return render(request, "pages/area_landing.html", {"city": city, "area": area})

    category = Category.objects.filter(slug=context_slug, is_active=True).first()
    if category:
        return render(request, "pages/city_category_landing.html", {"city": city, "category": category})

    raise Http404()


# =============================================================
# /s/{city}/{area}/{category}
# =============================================================
def area_category(request, city_slug, area_slug, category_slug):
    """
    URL: /s/{city}/{area}/{category}
    """
    city = get_object_or_404(City, slug=city_slug, is_active=True)
    area = get_object_or_404(Area, city=city, slug=area_slug, is_active=True)
    category = get_object_or_404(Category, slug=category_slug, is_active=True)

    return render(request, "pages/area_category_landing.html", {"city": city, "area": area, "category": category})
