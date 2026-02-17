from django.contrib import admin

from .models import SmsLog


@admin.register(SmsLog)
class SmsLogAdmin(admin.ModelAdmin):
    list_display = ("receptor", "message_short", "is_success", "created_at")
    list_filter = ("is_success", "created_at")
    search_fields = ("receptor", "message")
    readonly_fields = ("receptor", "message", "response_json", "is_success", "created_at")
    date_hierarchy = "created_at"

    def message_short(self, obj):
        return (obj.message[:60] + "…") if obj.message and len(obj.message) > 60 else (obj.message or "—")

    message_short.short_description = "محتوا"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
