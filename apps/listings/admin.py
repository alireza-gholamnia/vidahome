from django.contrib import admin
from django.utils.html import format_html

from .models import Listing, ListingImage


class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1
    fields = ("preview", "image", "alt", "sort_order", "is_cover")
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:6px;" />', obj.image.url)
        return "-"

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    inlines = [ListingImageInline]
    list_display = (
        "id",
        "title",
        "city",
        "agency",
        "deal",
        "status",
        "published_at",
        "_view_link",
    )

    def _view_link(self, obj):
        if obj and hasattr(obj, "get_absolute_url"):
            url = obj.get_absolute_url()
            return format_html(
                '<a href="{}" target="_blank" rel="noopener">مشاهده</a>',
                url,
            )
        return "-"

    _view_link.short_description = "مشاهده"
    list_filter = ("status", "deal", "city", "category")
    search_fields = ("id", "title", "slug")
    autocomplete_fields = ("city", "area", "category", "agency")

    fieldsets = (
        ("Listing Core", {
            "fields": (
                "title", "slug",
                ("city", "area", "category"),
                ("deal", "status", "published_at"),
                ("created_by", "agency"),
            )
        }),
        ("SEO (Optional Overrides)", {
            "fields": (
                "seo_title",
                "seo_meta_description",
                "seo_h1",
                "seo_canonical",
                ("seo_noindex", "allow_index"),
                "seo_priority",
            )
        }),
    )
