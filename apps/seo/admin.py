from django.contrib import admin
from django.utils.html import format_html

from apps.seo.models import CityCategory, CityCategoryImage, CityAreaCategory, CityAreaCategoryImage


def _view_link(obj):
    if obj and hasattr(obj, "get_absolute_url"):
        url = obj.get_absolute_url()
        return format_html(
            '<a href="{}" target="_blank" rel="noopener">مشاهده</a>',
            url,
        )
    return "-"


class CityCategoryImageInline(admin.TabularInline):
    model = CityCategoryImage
    extra = 0
    fields = ("image", "alt", "caption", "sort_order", "is_cover", "is_landing_cover", "is_content_image")
    ordering = ("sort_order", "id")


@admin.register(CityCategory)
class CityCategoryAdmin(admin.ModelAdmin):
    inlines = (CityCategoryImageInline,)
    list_display = (
        "city",
        "category",
        "is_active",
        "allow_index",
        "seo_noindex",
        "sort_order",
        "_view_link",
    )

    def _view_link(self, obj):
        return _view_link(obj)

    _view_link.short_description = "مشاهده"
    list_filter = ("is_active", "allow_index", "seo_noindex", "city", "category")
    search_fields = ("city__fa_name", "city__slug", "category__fa_name", "category__slug", "seo_title")
    ordering = ("city", "sort_order", "id")
    autocomplete_fields = ("city", "category")


class CityAreaCategoryImageInline(admin.TabularInline):
    model = CityAreaCategoryImage
    extra = 0
    fields = ("image", "alt", "caption", "sort_order", "is_cover", "is_landing_cover", "is_content_image")
    ordering = ("sort_order", "id")


@admin.register(CityAreaCategory)
class CityAreaCategoryAdmin(admin.ModelAdmin):
    inlines = (CityAreaCategoryImageInline,)
    list_display = (
        "city",
        "area",
        "category",
        "is_active",
        "allow_index",
        "seo_noindex",
        "sort_order",
        "_view_link",
    )

    def _view_link(self, obj):
        return _view_link(obj)

    _view_link.short_description = "مشاهده"
    list_filter = ("is_active", "allow_index", "seo_noindex", "city", "area", "category")
    search_fields = (
        "city__fa_name", "city__slug",
        "area__fa_name", "area__slug",
        "category__fa_name", "category__slug",
        "seo_title",
    )
    ordering = ("city", "area", "sort_order", "id")
    autocomplete_fields = ("city", "area", "category")
