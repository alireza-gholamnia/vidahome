from django.contrib import admin

from .models import Attribute, AttributeOption, ListingAttribute


class AttributeOptionInline(admin.TabularInline):
    model = AttributeOption
    extra = 1
    fields = ("value", "sort_order")
    ordering = ("sort_order", "id")


@admin.register(AttributeOption)
class AttributeOptionAdmin(admin.ModelAdmin):
    list_display = ("attribute", "value", "sort_order")
    list_filter = ("attribute",)
    search_fields = ("value",)
    autocomplete_fields = ("attribute",)


@admin.register(ListingAttribute)
class ListingAttributeAdmin(admin.ModelAdmin):
    list_display = ("listing", "attribute", "_attribute_categories", "value_int", "value_bool", "value_str", "value_option")
    list_filter = ("attribute",)

    def _attribute_categories(self, obj):
        if obj.attribute_id:
            names = list(obj.attribute.categories.values_list("fa_name", flat=True).order_by("fa_name"))
            return ", ".join(names) if names else "—"
        return "—"

    _attribute_categories.short_description = "دسته‌بندی ویژگی"
    search_fields = ("listing__title", "attribute__name")
    autocomplete_fields = ("listing", "attribute", "value_option")
    ordering = ("listing", "attribute__sort_order")


def _value_fields_for_type(value_type):
    """فقط فیلد مقدار متناسب با نوع ویژگی."""
    if value_type == Attribute.ValueType.INTEGER:
        return ("listing", "value_int")
    if value_type == Attribute.ValueType.BOOLEAN:
        return ("listing", "value_bool")
    if value_type == Attribute.ValueType.STRING:
        return ("listing", "value_str")
    if value_type == Attribute.ValueType.CHOICE:
        return ("listing", "value_option")
    return ("listing", "value_int", "value_bool", "value_str", "value_option")


class ListingAttributeInline(admin.TabularInline):
    model = ListingAttribute
    extra = 0
    fields = ("listing", "value_int", "value_bool", "value_str", "value_option")
    autocomplete_fields = ("listing", "value_option")

    def get_formset(self, request, obj=None, **kwargs):
        if obj and hasattr(obj, "value_type"):
            self.fields = _value_fields_for_type(obj.value_type)
        return super().get_formset(request, obj, **kwargs)


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "value_type", "unit", "sort_order", "is_active", "_categories_display", "_values_count")
    list_filter = ("value_type", "is_active")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("categories",)
    inlines = (AttributeOptionInline, ListingAttributeInline,)
    ordering = ("sort_order", "id")

    def _categories_count(self, obj):
        return obj.categories.count()

    _categories_count.short_description = "تعداد دسته‌ها"

    def _categories_display(self, obj):
        names = list(obj.categories.values_list("fa_name", flat=True).order_by("fa_name"))
        return ", ".join(names) if names else "—"

    _categories_display.short_description = "دسته‌بندی‌ها"

    def _values_count(self, obj):
        return obj.listing_values.count()

    _values_count.short_description = "تعداد مقادیر"
