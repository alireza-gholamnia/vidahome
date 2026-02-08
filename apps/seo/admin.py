from django.contrib import admin

from apps.seo.models import CityCategory, CityAreaCategory


@admin.register(CityCategory)
class CityCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "city",
        "category",
        "is_active",
        "allow_index",
        "seo_noindex",
        "sort_order",
    )
    list_filter = ("is_active", "allow_index", "seo_noindex", "city", "category")
    search_fields = ("city__fa_name", "city__slug", "category__fa_name", "category__slug", "seo_title")
    ordering = ("city", "sort_order", "id")
    autocomplete_fields = ("city", "category")


@admin.register(CityAreaCategory)
class CityAreaCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "city",
        "area",
        "category",
        "is_active",
        "allow_index",
        "seo_noindex",
        "sort_order",
    )
    list_filter = ("is_active", "allow_index", "seo_noindex", "city", "area", "category")
    search_fields = (
        "city__fa_name", "city__slug",
        "area__fa_name", "area__slug",
        "category__fa_name", "category__slug",
        "seo_title",
    )
    ordering = ("city", "area", "sort_order", "id")
    autocomplete_fields = ("city", "area", "category")
