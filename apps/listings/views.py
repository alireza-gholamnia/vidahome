from django.shortcuts import render, get_object_or_404
from apps.locations.models import City


def city_landing(request, city_slug):
    city = get_object_or_404(City, slug=city_slug, is_active=True)

    return render(
        request,
        "pages/city_landing.html",
        {
            "city": city,
        }
    )
