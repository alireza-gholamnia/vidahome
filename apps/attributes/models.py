from django.db import models

from .validators import validate_attribute_icon


class Attribute(models.Model):
    """
    تعریف ویژگی‌ها (مثل تعداد اتاق، متراژ، پارکینگ، نوع سند).
    هر ویژگی به یک یا چند دسته‌بندی متصل است و هنگام ثبت آگهی
    فقط ویژگی‌های مربوط به دسته‌ی آن آگهی نمایش داده می‌شوند.
    """

    class ValueType(models.TextChoices):
        INTEGER = "integer", "عددی"
        BOOLEAN = "boolean", "بله/خیر"
        CHOICE = "choice", "انتخابی"
        STRING = "string", "متن آزاد"

    name = models.CharField(max_length=120, verbose_name="نام فارسی")
    slug = models.SlugField(max_length=120, unique=True, verbose_name="اسلاگ")
    value_type = models.CharField(
        max_length=16,
        choices=ValueType.choices,
        verbose_name="نوع مقدار",
    )
    unit = models.CharField(
        max_length=32,
        blank=True,
        verbose_name="واحد",
        help_text="مثال: اتاق، متر، سال",
    )
    categories = models.ManyToManyField(
        "categories.Category",
        related_name="attributes",
        blank=True,
        verbose_name="دسته‌بندی‌ها",
        help_text="ویژگی فقط برای این دسته‌ها نمایش داده می‌شود",
    )
    sort_order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    is_filterable = models.BooleanField(
        default=False,
        verbose_name="نمایش در فیلترها",
        help_text="اگر فعال باشد، این ویژگی در سایدبار فیلتر صفحه آگهی‌ها نمایش داده می‌شود",
    )
    icon = models.FileField(
        upload_to="attribute_icons/",
        blank=True,
        null=True,
        verbose_name="آیکون",
        help_text="فقط PNG یا SVG، حداکثر ۶۴ کیلوبایت، ابعاد حداکثر ۱۲۸×۱۲۸",
        validators=[validate_attribute_icon],
    )

    class Meta:
        ordering = ("sort_order", "id")
        verbose_name = "ویژگی"
        verbose_name_plural = "ویژگی‌ها"

    def __str__(self):
        return self.name


class AttributeOption(models.Model):
    """
    مقادیر از پیش تعریف‌شده برای هر ویژگی.
    مثلاً برای «تعداد اتاق»: 1، 2، 3، 4، ...
    """
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name="options",
        verbose_name="ویژگی",
    )
    value = models.CharField(max_length=120, verbose_name="مقدار")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="ترتیب")

    class Meta:
        ordering = ("sort_order", "id")
        verbose_name = "گزینه ویژگی"
        verbose_name_plural = "گزینه‌های ویژگی"
        unique_together = [("attribute", "value")]

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class ListingAttribute(models.Model):
    """
    مقدار هر ویژگی برای هر آگهی.
    بر اساس value_type مربوط به Attribute، فقط یکی از فیلدهای value_*
    مقدار می‌گیرد.
    """
    listing = models.ForeignKey(
        "listings.Listing",
        on_delete=models.CASCADE,
        related_name="attribute_values",
        verbose_name="آگهی",
    )
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name="listing_values",
        verbose_name="ویژگی",
    )
    value_int = models.IntegerField(null=True, blank=True, verbose_name="مقدار عددی")
    value_bool = models.BooleanField(null=True, blank=True, verbose_name="مقدار بله/خیر")
    value_str = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="مقدار متن",
        help_text="برای عددی از value_int، برای بله/خیر از value_bool استفاده شود",
    )
    value_option = models.ForeignKey(
        "AttributeOption",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="listing_values",
        verbose_name="مقدار انتخابی",
    )

    class Meta:
        ordering = ("attribute__sort_order", "attribute_id")
        verbose_name = "ویژگی آگهی"
        verbose_name_plural = "ویژگی‌های آگهی"
        unique_together = [("listing", "attribute")]

    def __str__(self):
        return f"{self.listing.title} — {self.attribute.name}: {self.display_value}"

    @property
    def display_value(self):
        """مقدار قابل نمایش برای کاربر."""
        if self.value_int is not None:
            unit = f" {self.attribute.unit}" if self.attribute.unit else ""
            return f"{self.value_int}{unit}"
        if self.value_bool is not None:
            return "بله" if self.value_bool else "خیر"
        if self.value_str:
            return self.value_str
        if self.value_option_id:
            return self.value_option.value
        return "—"
