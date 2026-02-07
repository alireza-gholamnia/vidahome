from django.shortcuts import render, get_object_or_404
from apps.locations.models import City, Area


def city_landing(request, city_slug):
    city = get_object_or_404(City, slug=city_slug, is_active=True)

    areas = (
        Area.objects
        .filter(city=city, is_active=True)
        .order_by("sort_order", "id")
    )

    return render(
        request,
        "pages/city_landing.html",
        {"city": city, "areas": areas}
    )

def area_landing(request, city_slug, area_slug):
    city = get_object_or_404(City, slug=city_slug, is_active=True)
    area = get_object_or_404(Area, city=city, slug=area_slug, is_active=True)

    return render(
        request,
        "pages/area_landing.html",
        {"city": city, "area": area}
    )