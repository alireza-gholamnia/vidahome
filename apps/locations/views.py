from django.shortcuts import render
from .models import City


def cities_directory(request):
    cities = (
        City.objects
        .filter(is_active=True)
        .order_by("sort_order", "id")
    )
    return render(request, "pages/cities.html", {"cities": cities})
