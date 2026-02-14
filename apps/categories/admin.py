from django.contrib import admin
from django.utils.html import format_html
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("fa_name", "en_name", "slug", "parent", "is_active", "sort_order", "_view_link")

    def _view_link(self, obj):
        if obj and hasattr(obj, "get_absolute_url"):
            url = obj.get_absolute_url()
            return format_html(
                '<a href="{}" target="_blank" rel="noopener">مشاهده</a>',
                url,
            )
        return "-"

    _view_link.short_description = "مشاهده"
    list_filter = ("is_active", "parent")
    search_fields = ("fa_name", "en_name", "slug")
    ordering = ("parent_id", "sort_order", "id")
    prepopulated_fields = {"slug": ("en_name",)}
