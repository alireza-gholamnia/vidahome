"""ادمین لیدها — نمایش یکپارچه با منبع صفحه."""
from django.contrib import admin
from .models import ListingLead, LandingLead


@admin.register(ListingLead)
class ListingLeadAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "get_source", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "phone", "message")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

    def get_source(self, obj):
        return f"آگهی: {obj.listing.title[:40]}..." if obj.listing else "-"
    get_source.short_description = "صفحه مبدا"


@admin.register(LandingLead)
class LandingLeadAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "get_source", "status", "created_at")
    list_filter = ("source_type", "status", "created_at")
    search_fields = ("name", "phone", "email", "message")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
    list_editable = ("status",)

    def get_source(self, obj):
        return obj.get_source_display()
    get_source.short_description = "صفحه مبدا"
