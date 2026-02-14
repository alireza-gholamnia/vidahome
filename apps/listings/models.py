from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils import timezone

from ckeditor.fields import RichTextField
from apps.seo.base import BaseSEO
from apps.common.upload_utils import listing_image_upload_to


class Listing(BaseSEO, models.Model):
    # =====================================================
    # Enums
    # =====================================================
    class Deal(models.TextChoices):
        BUY = "buy", "Buy"
        RENT = "rent", "Rent"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"

    # =====================================================
    # Core Identity
    # =====================================================
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, db_index=True)

    # =====================================================
    # Location & Category (Search backbone)
    # =====================================================
    city = models.ForeignKey(
        "locations.City",
        on_delete=models.PROTECT,
        related_name="listings",
    )

    area = models.ForeignKey(
        "locations.Area",
        on_delete=models.PROTECT,
        related_name="listings",
        null=True,
        blank=True,
    )

    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.PROTECT,
        related_name="listings",
    )

    # =====================================================
    # Deal & Lifecycle
    # =====================================================
    deal = models.CharField(
        max_length=10,
        choices=Deal.choices,
        default=Deal.BUY,
        db_index=True,
    )

    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )

    published_at = models.DateTimeField(null=True, blank=True)

    # =====================================================
    # Content (Human-readable)
    # =====================================================
    short_description = models.TextField(
        blank=True,
        help_text="Short summary for meta description / cards"
    )

    description = RichTextField(
        blank=True,
        help_text="Main listing description"
    )

    # =====================================================
    # Optional Pricing (generic – not opinionated)
    # =====================================================
    price = models.BigIntegerField(
        null=True,
        blank=True,
        help_text="Main price (buy or rent)"
    )

    price_unit = models.CharField(
        max_length=32,
        blank=True,
        help_text="e.g. تومان / دلار / متر"
    )

    # =====================================================
    # Creator & Agency
    # =====================================================
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="listings",
    )
    agency = models.ForeignKey(
        "agencies.Agency",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="listings",
    )

    # =====================================================
    # Timestamps
    # =====================================================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # =====================================================
    # Meta
    # =====================================================
    class Meta:
        ordering = ("-published_at", "-id")
        indexes = [
            models.Index(fields=["status", "deal"]),
            models.Index(fields=["city", "area", "category"]),
            models.Index(fields=["published_at"]),
            models.Index(fields=["slug"]),
        ]

    # =====================================================
    # Helpers
    # =====================================================
    def __str__(self):
        return f"{self.title} ({self.id})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:255]

        # Auto publish timestamp
        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/l/{self.id}-{self.slug}/"



class ListingImage(models.Model):
    listing = models.ForeignKey(
        "listings.Listing",
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = models.ImageField(upload_to=listing_image_upload_to)
    alt = models.CharField(max_length=180, blank=True)

    sort_order = models.PositiveIntegerField(default=0)
    is_cover = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("sort_order", "id")
        indexes = [
            models.Index(fields=["listing", "sort_order"]),
            models.Index(fields=["listing", "is_cover"]),
        ]

    def __str__(self):
        return f"Image {self.id} for Listing {self.listing_id}"
