from django.contrib import admin
from .models import Province, City, Area


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ("fa_name", "en_name", "slug", "is_active", "sort_order")
    list_filter = ("is_active",)
    search_fields = ("fa_name", "en_name", "slug")
    ordering = ("sort_order", "id")
    prepopulated_fields = {"slug": ("en_name",)}


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("fa_name", "en_name", "slug", "province", "is_active", "sort_order")
    list_filter = ("province", "is_active")
    search_fields = ("fa_name", "en_name", "slug")
    ordering = ("province", "sort_order", "id")
    prepopulated_fields = {"slug": ("en_name",)}


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ("fa_name", "en_name", "slug", "city", "is_active", "sort_order")
    list_filter = ("city", "is_active")
    search_fields = ("fa_name", "en_name", "slug")
    ordering = ("city", "sort_order", "id")
    prepopulated_fields = {"slug": ("en_name",)}
