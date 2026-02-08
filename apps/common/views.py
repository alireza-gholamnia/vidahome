from django.shortcuts import render
from django.apps import apps

def home(request):
    City = apps.get_model("locations", "City")
    Category = apps.get_model("categories", "Category")

    top_cities = City.objects.filter(is_active=True).order_by("sort_order")[:12]
    top_categories = Category.objects.filter(is_active=True, parent__isnull=True).order_by("sort_order")[:12]

    return render(
        request,
        "pages/home.html",
        {
            "top_cities": top_cities,
            "top_categories": top_categories,
        },
    )
