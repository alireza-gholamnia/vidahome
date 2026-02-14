from django.contrib import admin
from django.utils.html import format_html
from .models import Province, City, Area


def _view_link(url):
    """لینک مشاهده در سایت"""
    if url:
        return format_html(
            '<a href="{}" target="_blank" rel="noopener">مشاهده</a>',
            url,
        )
    return "-"


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ("fa_name", "en_name", "slug", "is_active", "sort_order", "_view_link")

    def _view_link(self, obj):
        return _view_link(obj.get_absolute_url() if obj else None)

    _view_link.short_description = "مشاهده"
    list_filter = ("is_active",)
    search_fields = ("fa_name", "en_name", "slug")
    ordering = ("sort_order", "id")
    prepopulated_fields = {"slug": ("en_name",)}


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("fa_name", "en_name", "slug", "province", "is_active", "sort_order", "_view_link")

    def _view_link(self, obj):
        return _view_link(obj.get_absolute_url() if obj else None)

    _view_link.short_description = "مشاهده"
    list_filter = ("province", "is_active")
    search_fields = ("fa_name", "en_name", "slug")
    ordering = ("province", "sort_order", "id")
    prepopulated_fields = {"slug": ("en_name",)}

    fieldsets = (
        (
            "اطلاعات اصلی",
            {
                "fields": ("fa_name", "en_name", "slug", "province", "is_active", "sort_order"),
                "description": "نام و شناسه شهر — این موارد اولویت نمایش دارند.",
            },
        ),
        (
            "محتوای صفحه",
            {
                "fields": ("intro_content", "main_content"),
                "description": "متن معرفی و محتوای اصلی صفحه شهر.",
            },
        ),
        (
            "تنظیمات سئو",
            {
                "fields": (
                    "seo_title",
                    "seo_meta_description",
                    "seo_h1",
                    "seo_canonical",
                    "seo_noindex",
                    "allow_index",
                    "seo_priority",
                ),
                "classes": ("collapse",),
                "description": "عنوان، توضیحات متا و تنظیمات ایندکس — اختیاری.",
            },
        ),
    )


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ("fa_name", "en_name", "slug", "city", "is_active", "sort_order", "_view_link")

    def _view_link(self, obj):
        return _view_link(obj.get_absolute_url() if obj else None)

    _view_link.short_description = "مشاهده"
    list_filter = ("city", "is_active")
    search_fields = ("fa_name", "en_name", "slug")
    ordering = ("city", "sort_order", "id")
    prepopulated_fields = {"slug": ("en_name",)}

    fieldsets = (
        (
            "اطلاعات اصلی",
            {
                "fields": ("fa_name", "en_name", "slug", "city", "is_active", "sort_order"),
                "description": "نام و شناسه محله.",
            },
        ),
        (
            "محتوای صفحه",
            {
                "fields": ("intro_content", "main_content"),
            },
        ),
        (
            "تنظیمات سئو",
            {
                "fields": (
                    "seo_title",
                    "seo_meta_description",
                    "seo_h1",
                    "seo_canonical",
                    "seo_noindex",
                    "allow_index",
                    "seo_priority",
                ),
                "classes": ("collapse",),
            },
        ),
    )
