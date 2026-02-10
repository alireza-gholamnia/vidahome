from django.contrib import admin
from .models import Listing
from .models import Listing, ListingImage
from django.utils.html import format_html


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
    list_display = ("id", "title", "city", "area", "category", "deal", "status", "published_at")
    list_filter = ("status", "deal", "city", "category")
    search_fields = ("id", "title", "slug")
    autocomplete_fields = ("city", "area", "category")

    fieldsets = (
        ("Listing Core", {
            "fields": (
                "title", "slug",
                ("city", "area", "category"),
                ("deal", "status", "published_at"),
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
