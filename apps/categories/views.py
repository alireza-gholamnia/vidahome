from django.shortcuts import render

from .models import Category


def categories_directory(request):
    property_categories = (
        Category.property_queryset()
        .prefetch_related("images", "children")
        .filter(parent__isnull=True, is_active=True)
        .order_by("sort_order", "fa_name")
    )
    project_categories = (
        Category.objects.filter(
            category_type=Category.CategoryType.PROJECT,
            parent__isnull=True,
            is_active=True,
        )
        .prefetch_related("images", "children")
        .order_by("sort_order", "fa_name")
    )
    service_categories = (
        Category.objects.filter(
            category_type=Category.CategoryType.SERVICE,
            parent__isnull=True,
            is_active=True,
        )
        .prefetch_related("images", "children")
        .order_by("sort_order", "fa_name")
    )

    breadcrumbs = [
        {"title": "صفحه اصلی", "url": "/"},
        {"title": "دسته‌بندی‌ها", "url": None},
    ]

    return render(
        request,
        "pages/categories.html",
        {
            "property_categories": property_categories,
            "project_categories": project_categories,
            "service_categories": service_categories,
            "breadcrumbs": breadcrumbs,
        },
    )
