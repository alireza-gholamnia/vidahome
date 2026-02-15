import json

from django import forms
from django.contrib import admin
from django.utils.html import format_html

from apps.attributes.models import Attribute, AttributeOption, ListingAttribute

from .models import Listing, ListingImage


class ListingAttributeForm(forms.ModelForm):
    """فرم با فیلد مخفی برای شناسایی attribute و غیرفعال کردن ورودی‌های نامربوط."""
    _attr_id = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = ListingAttribute
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.attribute_id:
            self.fields["_attr_id"].initial = str(self.instance.attribute_id)
            # فیلتر value_option بر اساس attribute
            if self.instance.attribute.value_type == Attribute.ValueType.CHOICE:
                self.fields["value_option"].queryset = AttributeOption.objects.filter(
                    attribute=self.instance.attribute,
                ).order_by("sort_order", "id")


class ListingAttributeInline(admin.TabularInline):
    model = ListingAttribute
    form = ListingAttributeForm
    extra = 0
    fields = ("attribute", "_attr_id", "value_int", "value_bool", "value_str", "value_option")
    verbose_name = "ویژگی آگهی"
    verbose_name_plural = "ویژگی‌های آگهی"
    # value_option بدون autocomplete تا فیلتر گزینه‌ها بر اساس attribute درست کار کند
    readonly_fields = ("attribute",)

    def has_add_permission(self, request, obj=None):
        # ردیف‌ها توسط سینگال همگام‌سازی ایجاد می‌شوند
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        # فیلتر value_option بر اساس attribute در هر ردیف (در فرم انجام می‌شود)
        return formset


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
    change_form_template = "admin/listings/listing/change_form.html"
    inlines = [ListingAttributeInline, ListingImageInline]

    def _listing_attrs_context(self, obj):
        """مقدار context برای ویژگی‌ها و گزینه‌ها."""
        if not obj or not obj.category_id:
            return {
                "attribute_value_types_json": "{}",
                "attribute_options_json": "{}",
            }
        attrs = Attribute.objects.filter(
            categories=obj.category,
        ).values("id", "value_type")
        value_types = {str(a["id"]): a["value_type"] for a in attrs}
        attr_ids = [a["id"] for a in attrs]
        options_map = {}
        for opt in AttributeOption.objects.filter(
            attribute_id__in=attr_ids,
        ).order_by("attribute_id", "sort_order", "id").values("attribute_id", "value"):
            aid = str(opt["attribute_id"])
            if aid not in options_map:
                options_map[aid] = []
            options_map[aid].append(opt["value"])
        return {
            "attribute_value_types_json": json.dumps(value_types),
            "attribute_options_json": json.dumps(options_map),
        }

    def add_view(self, request, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["attribute_value_types_json"] = "{}"
        extra_context["attribute_options_json"] = "{}"
        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        obj = self.get_object(request, object_id)
        extra_context.update(self._listing_attrs_context(obj))
        return super().change_view(request, object_id, form_url, extra_context)
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
