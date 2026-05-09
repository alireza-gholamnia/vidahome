from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Agency,
    AgencyImage,
    AgencyMembership,
    AgencyJoinRequest,
    AgencyEmployeeInvite,
    EmployeeRemoveRequest,
)


def _view_link(url):
    if url:
        return format_html('<a href="{}" target="_blank" rel="noopener">مشاهده</a>', url)
    return "-"


class AgencyImageInline(admin.TabularInline):
    model = AgencyImage
    extra = 0
    fields = ("image", "alt", "caption", "sort_order", "is_cover", "is_landing_cover")
    ordering = ("sort_order", "id")


class AgencyMembershipInline(admin.TabularInline):
    model = AgencyMembership
    extra = 0
    fields = ("user", "role", "status", "created_by", "joined_at", "left_at")
    autocomplete_fields = ("user", "created_by")
    readonly_fields = ("joined_at",)
    ordering = ("role", "user__username")


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "owner", "phone", "approval_status", "is_active", "_view_link")
    list_filter = ("is_active", "approval_status")
    search_fields = ("name", "slug", "owner__username")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("cities",)
    inlines = (AgencyMembershipInline, AgencyImageInline)

    fieldsets = (
        ("اطلاعات اصلی", {"fields": ("name", "slug", "owner", "phone", "address", "approval_status", "is_active")}),
        ("محتوای لندینگ", {"fields": ("intro_content", "main_content", "logo")}),
        ("شهرهای تحت فعالیت", {"fields": ("cities",)}),
        ("سئو", {"fields": ("seo_title", "seo_meta_description", "seo_h1", "seo_canonical", "seo_noindex", "allow_index", "seo_priority"), "classes": ("collapse",)}),
    )

    def _view_link(self, obj):
        return _view_link(obj.get_absolute_url() if obj else None)

    _view_link.short_description = "مشاهده"


@admin.register(AgencyMembership)
class AgencyMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "agency", "role", "status", "joined_at", "left_at")
    list_filter = ("role", "status", "agency")
    search_fields = ("user__username", "user__phone", "agency__name")
    autocomplete_fields = ("user", "agency", "created_by")
    readonly_fields = ("created_at", "updated_at")


@admin.register(AgencyJoinRequest)
class AgencyJoinRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "agency", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("user__username", "agency__name")
    readonly_fields = ("created_at", "reviewed_at")


@admin.register(AgencyEmployeeInvite)
class AgencyEmployeeInviteAdmin(admin.ModelAdmin):
    list_display = ("invited_user", "agency", "invited_by", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("invited_user__username", "agency__name", "invited_by__username")
    readonly_fields = ("created_at", "responded_at")


@admin.register(EmployeeRemoveRequest)
class EmployeeRemoveRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "agency", "requested_by", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("user__username", "agency__name")
