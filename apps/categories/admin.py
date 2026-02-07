from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("fa_name", "en_name", "slug", "parent", "is_active", "sort_order")
    list_filter = ("is_active", "parent")
    search_fields = ("fa_name", "en_name", "slug")
    ordering = ("parent_id", "sort_order", "id")
    prepopulated_fields = {"slug": ("en_name",)}
