from django.contrib import admin
from .models import Listing


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
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
