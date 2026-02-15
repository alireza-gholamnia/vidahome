from django.db.models import Count, Q
from django.shortcuts import render
from .models import City


def cities_directory(request):
    cities = (
        City.objects
        .filter(is_active=True)
        .select_related("province")
        .prefetch_related("images")
        .annotate(listing_count=Count("listings", filter=Q(listings__status="published")))
        .order_by("sort_order", "id")
    )
    breadcrumbs = [
        {"title": "صفحه اصلی", "url": "/"},
        {"title": "شهرها", "url": None},
    ]
    return render(request, "pages/cities.html", {"cities": cities, "breadcrumbs": breadcrumbs})
