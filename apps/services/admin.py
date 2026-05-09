from django import forms
from django.contrib import admin
from django.utils.html import format_html

from apps.categories.models import Category

from .models import ServiceProvider, ServiceProviderImage


class ServiceProviderForm(forms.ModelForm):
    class Meta:
        model = ServiceProvider
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["categories"].queryset = Category.objects.filter(
            category_type=Category.CategoryType.SERVICE,
            is_active=True,
        ).order_by("sort_order", "fa_name")

    def clean_categories(self):
        categories = self.cleaned_data["categories"]
        invalid = categories.exclude(category_type=Category.CategoryType.SERVICE)
        if invalid.exists():
            raise forms.ValidationError("فقط دسته‌بندی‌های نوع سرویس قابل انتخاب هستند.")
        return categories


class ServiceProviderImageInline(admin.TabularInline):
    model = ServiceProviderImage
    extra = 0
    fields = ("image", "alt", "caption", "sort_order", "is_cover", "is_landing_cover")
    ordering = ("sort_order", "id")


@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    form = ServiceProviderForm
    inlines = (ServiceProviderImageInline,)
    list_display = (
        "name",
        "provider_type",
        "approval_status",
        "is_active",
        "_categories",
        "phone",
        "mobile",
        "_view_link",
    )
    list_filter = ("provider_type", "approval_status", "is_active", "categories", "cities")
    search_fields = ("name", "slug", "phone", "mobile", "email")
    filter_horizontal = ("categories", "cities")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name", "id")

    def _categories(self, obj):
        return "، ".join(obj.categories.values_list("fa_name", flat=True)[:3]) or "-"

    _categories.short_description = "دسته‌ها"

    def _view_link(self, obj):
        if obj and obj.pk:
            return format_html('<a href="{}" target="_blank" rel="noopener">مشاهده</a>', obj.get_absolute_url())
        return "-"

    _view_link.short_description = "مشاهده"


@admin.register(ServiceProviderImage)
class ServiceProviderImageAdmin(admin.ModelAdmin):
    list_display = ("provider", "alt", "sort_order", "is_cover", "is_landing_cover")
    list_filter = ("is_cover", "is_landing_cover")
    search_fields = ("provider__name", "alt", "caption")
    ordering = ("provider", "sort_order", "id")
