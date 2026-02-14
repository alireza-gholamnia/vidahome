from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError

from ckeditor.fields import RichTextField
from apps.seo.base import BaseSEO
from django.apps import apps



# =====================================================
# Base Location (abstract)
# =====================================================

class BaseLocation(models.Model):
    """
    Abstract base model for all location entities.

    VidaHome rules:
    - Province is DB-only (NOT in URL).
    - City.slug must be GLOBAL UNIQUE (because /s/{city} exists).
    - Area.slug must be UNIQUE PER CITY (because /s/{city}/{area} exists).
    """

    fa_name = models.CharField(
        max_length=120,
        help_text="Persian display name"
    )

    en_name = models.CharField(
        max_length=120,
        help_text="English name used for slug generation"
    )

    slug = models.SlugField(
        max_length=140,
        db_index=True,
        help_text="SEO-friendly URL slug"
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Controls visibility in public pages"
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        help_text="Ordering priority"
    )

    class Meta:
        abstract = True
        ordering = ("sort_order", "id")

    def __str__(self):
        return self.fa_name


# =====================================================
# Province (DB-only)
# =====================================================

class Province(BaseLocation):
    """
    DB-only taxonomy level (NOT used in URL paths).
    Useful for admin organization and analytics.
    """

    class Meta(BaseLocation.Meta):
        verbose_name = "Province"
        verbose_name_plural = "Provinces"
        constraints = [
            models.UniqueConstraint(
                fields=["slug"],
                name="uniq_province_slug"
            ),
            models.UniqueConstraint(
                fields=["en_name"],
                name="uniq_province_en_name"
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.en_name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return "/cities/"


# =====================================================
# City
# =====================================================

class City(BaseLocation, BaseSEO):
    """
    City appears in URL path: /s/{city}
    Therefore City.slug MUST be globally unique.
    """

    province = models.ForeignKey(
        Province,
        on_delete=models.PROTECT,
        related_name="cities",
        help_text="DB-only grouping; not used in URL"
    )

    # --- Landing content ---
    intro_content = models.TextField(
        blank=True,
        help_text="Short intro shown at top of city landing page"
    )

    main_content = RichTextField(
        blank=True,
        help_text="Main city landing content"
    )

    class Meta(BaseLocation.Meta):
        verbose_name = "City"
        verbose_name_plural = "Cities"
        constraints = [
            models.UniqueConstraint(
                fields=["slug"],
                name="uniq_city_slug"
            ),
            models.UniqueConstraint(
                fields=["en_name"],
                name="uniq_city_en_name"
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.en_name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/s/{self.slug}/"


# =====================================================
# Area
# =====================================================

class Area(BaseLocation, BaseSEO):
    """
    Area appears in URL path under a city: /s/{city}/{area}
    Therefore Area.slug MUST be unique per city.
    """

    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        related_name="areas"
    )

    # --- Landing content ---
    intro_content = models.TextField(
        blank=True,
        help_text="Short intro shown at top of area landing page"
    )

    main_content = RichTextField(
        blank=True,
        help_text="Main area landing content"
    )

    class Meta(BaseLocation.Meta):
        verbose_name = "Area"
        verbose_name_plural = "Areas"
        constraints = [
            models.UniqueConstraint(
                fields=["city", "slug"],
                name="uniq_area_slug_in_city"
            ),
            models.UniqueConstraint(
                fields=["city", "en_name"],
                name="uniq_area_en_name_in_city"
            ),
        ]

    def clean(self):
        """
        Prevent Area.slug collision with Category slugs.
        This avoids ambiguity in:
        /s/{city}/{context}
        where context can be Area or Category.
        """
        if self.slug and Category.objects.filter(slug=self.slug).exists():
            raise ValidationError({
                "slug": "This slug is reserved for categories. Choose a different slug for Area."
            })


    def clean(self):
        """
        Prevent Area.slug collision with Category slugs.
        This avoids ambiguity in:
        /s/{city}/{context}
        where context can be Area or Category.
        """
        Category = apps.get_model("categories", "Category")
        if self.slug and Category.objects.filter(slug=self.slug).exists():
            raise ValidationError({
                "slug": "This slug is reserved for categories. Choose a different slug for Area."
            })

    def get_absolute_url(self):
        return f"/s/{self.city.slug}/{self.slug}/"
