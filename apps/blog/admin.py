from django.contrib import admin
from django.utils.html import format_html

from apps.categories.models import Category
from .models import BlogCategory, BlogPost


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("fa_name", "slug", "is_active", "sort_order", "_post_count")
    list_filter = ("is_active",)
    search_fields = ("fa_name", "slug")

    def _post_count(self, obj):
        return obj.posts.count()

    _post_count.short_description = "تعداد پست"


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "blog_category", "status", "published_at", "city", "listing_category", "_view_link")
    list_filter = ("status", "blog_category")
    search_fields = ("title", "excerpt")
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("author",)
    autocomplete_fields = ("blog_category", "city", "area", "listing_category")
    date_hierarchy = "published_at"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "listing_category":
            kwargs["queryset"] = Category.landing_queryset().filter(is_active=True).order_by("sort_order", "fa_name")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    fieldsets = (
        (None, {"fields": ("title", "slug", "excerpt", "content", "cover_image", "status", "published_at", "author")}),
        ("دسته‌بندی بلاگ", {"fields": ("blog_category",)}),
        ("ارتباط با لندینگ‌ها", {"fields": ("city", "area", "listing_category")}),
        ("سئو", {"fields": ("seo_title", "seo_meta_description", "seo_h1", "seo_canonical", "seo_noindex", "allow_index")}),
    )

    def _view_link(self, obj):
        if obj and obj.slug:
            url = obj.get_absolute_url()
            return format_html('<a href="{}" target="_blank" rel="noopener">مشاهده</a>', url)
        return "-"

    _view_link.short_description = "مشاهده"
