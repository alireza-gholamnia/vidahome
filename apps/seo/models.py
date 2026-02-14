from django.db import models
from django.core.exceptions import ValidationError

from ckeditor_uploader.fields import RichTextUploadingField

from apps.seo.base import BaseSEO
from apps.common.upload_utils import city_category_image_upload_to, area_category_image_upload_to
from apps.locations.models import City, Area
from apps.categories.models import Category


# =====================================================
# City + Category
# URL: /s/{city}/{category}/
# =====================================================

class CityCategory(BaseSEO):
    """
    SEO + Content override for:
    /s/{city}/{category}/
    """

    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="seo_city_categories"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="seo_city_categories"
    )

    intro_content = models.TextField(
        blank=True,
        help_text="Intro content shown above listings"
    )

    main_content = RichTextUploadingField(
        blank=True,
        help_text="محتوا با امکان درج و آپلود تصویر",
    )

    is_active = models.BooleanField(
        default=True,
        help_text="If false, this override will be ignored"
    )

    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("sort_order", "id")
        constraints = [
            models.UniqueConstraint(
                fields=["city", "category"],
                name="uniq_city_category_landing"
            )
        ]

    def __str__(self):
        return f"{self.category.fa_name} در {self.city.fa_name}"

    def get_absolute_url(self):
        return f"/s/{self.city.slug}/{self.category.slug}/"

    def get_cover_image(self):
        images = list(self.images.all())
        for img in images:
            if img.is_cover:
                return img
        return images[0] if images else None

    def get_landing_cover_image(self):
        images = list(self.images.all())
        for img in images:
            if img.is_landing_cover:
                return img
        return images[0] if images else None


class CityCategoryImage(models.Model):
    """گالری تصاویر لندینگ شهر + دسته."""
    city_category = models.ForeignKey(
        CityCategory,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to=city_category_image_upload_to)
    alt = models.CharField(max_length=180, blank=True)
    caption = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_cover = models.BooleanField(default=False)
    is_landing_cover = models.BooleanField(default=False, help_text="کاور صفحه لندینگ")
    is_content_image = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("sort_order", "id")
        verbose_name = "تصویر شهر+دسته"
        verbose_name_plural = "تصاویر شهر+دسته"

    def __str__(self):
        return f"Image for {self.city_category}"


# =====================================================
# City + Area + Category
# URL: /s/{city}/{area}/{category}/
# =====================================================

class CityAreaCategory(BaseSEO):
    """
    SEO + Content override for:
    /s/{city}/{area}/{category}/
    """

    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="seo_area_categories"
    )

    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        related_name="seo_area_categories"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="seo_area_categories"
    )

    intro_content = models.TextField(
        blank=True,
        help_text="Intro content shown above listings"
    )

    main_content = RichTextUploadingField(
        blank=True,
        help_text="محتوا با امکان درج و آپلود تصویر",
    )

    is_active = models.BooleanField(
        default=True,
        help_text="If false, this override will be ignored"
    )

    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("sort_order", "id")
        constraints = [
            models.UniqueConstraint(
                fields=["area", "category"],
                name="uniq_area_category_landing"
            )
        ]

    def clean(self):
        """
        Ensure area belongs to selected city.
        """
        if self.area.city_id != self.city_id:
            raise ValidationError({
                "area": "Selected area does not belong to the selected city."
            })

    def __str__(self):
        return f"{self.category.fa_name} در {self.area.fa_name} ({self.city.fa_name})"

    def get_absolute_url(self):
        return f"/s/{self.city.slug}/{self.area.slug}/{self.category.slug}/"

    def get_cover_image(self):
        images = list(self.images.all())
        for img in images:
            if img.is_cover:
                return img
        return images[0] if images else None

    def get_landing_cover_image(self):
        images = list(self.images.all())
        for img in images:
            if img.is_landing_cover:
                return img
        return images[0] if images else None


class CityAreaCategoryImage(models.Model):
    """گالری تصاویر لندینگ محله + دسته."""
    city_area_category = models.ForeignKey(
        CityAreaCategory,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to=area_category_image_upload_to)
    alt = models.CharField(max_length=180, blank=True)
    caption = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_cover = models.BooleanField(default=False)
    is_landing_cover = models.BooleanField(default=False, help_text="کاور صفحه لندینگ")
    is_content_image = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("sort_order", "id")
        verbose_name = "تصویر محله+دسته"
        verbose_name_plural = "تصاویر محله+دسته"

    def __str__(self):
        return f"Image for {self.city_area_category}"
