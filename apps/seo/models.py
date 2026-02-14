from django.db import models
from django.core.exceptions import ValidationError

from ckeditor.fields import RichTextField

from apps.seo.base import BaseSEO
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

    main_content = RichTextField(
        blank=True,
        help_text="Main SEO content for city+category landing"
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

    main_content = RichTextField(
        blank=True,
        help_text="Main SEO content for area+category landing"
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
