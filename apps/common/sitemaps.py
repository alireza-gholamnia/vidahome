"""Sitemap برای SEO."""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.apps import apps


class StaticSitemap(Sitemap):
    """صفحات استاتیک."""
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ["home", "listing_catalog", "agency_list", "agent_list", "contact"]

    def location(self, item):
        return reverse(item)


class ListingSitemap(Sitemap):
    """آگهی‌های منتشرشده."""
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        Listing = apps.get_model("listings", "Listing")
        return (
            Listing.objects.filter(status="published")
            .select_related("city", "category")
            .order_by("-published_at", "-id")
        )

    def lastmod(self, obj):
        return obj.updated_at


class CitySitemap(Sitemap):
    """شهرها."""
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        City = apps.get_model("locations", "City")
        return City.objects.filter(is_active=True).order_by("sort_order")

    def location(self, obj):
        return obj.get_absolute_url()


class CategorySitemap(Sitemap):
    """دسته‌بندی‌ها (فقط والد)."""
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        Category = apps.get_model("categories", "Category")
        return Category.objects.filter(parent__isnull=True, is_active=True).order_by("sort_order")

    def location(self, obj):
        return obj.get_absolute_url()


class AgencySitemap(Sitemap):
    """مشاوره‌های املاک فعال."""
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        Agency = apps.get_model("agencies", "Agency")
        return (
            Agency.objects.filter(is_active=True, approval_status="approved")
            .order_by("id")
        )

    def location(self, obj):
        return obj.get_absolute_url()


class BlogPostSitemap(Sitemap):
    """پست‌های بلاگ."""
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        BlogPost = apps.get_model("blog", "BlogPost")
        return (
            BlogPost.objects.filter(status="published")
            .order_by("-published_at", "-id")
        )

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, "updated_at") else obj.published_at
