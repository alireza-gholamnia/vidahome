from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import User

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """ادمین کاربر با فیلدهای پروفایل و گروه‌ها."""
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "_role", "agency", "phone", "is_verified")
    list_filter = ("is_staff", "is_superuser", "is_active", "is_verified", "groups")
    search_fields = ("username", "email", "first_name", "last_name", "phone")
    autocomplete_fields = ("agency",)

    fieldsets = BaseUserAdmin.fieldsets + (
        ("پروفایل", {"fields": ("phone", "agency", "avatar", "is_verified")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("پروفایل", {"fields": ("phone", "agency", "avatar", "is_verified")}),
    )

    def _role(self, obj):
        return obj.get_role_display()

    _role.short_description = "نقش (از گروه)"
