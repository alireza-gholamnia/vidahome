from django.shortcuts import render
from .models import Category

def categories_directory(request):
    categories = (
        Category.objects
        .filter(parent__isnull=True, is_active=True)
        .prefetch_related("children")
        .order_by("sort_order", "fa_name")   # ✅ به جای name
    )

    return render(request, "pages/categories.html", {"categories": categories})
