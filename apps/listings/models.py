from django.conf import settings
from django.db import models
from django.utils import timezone

from ckeditor.fields import RichTextField

from apps.common.text_utils import slugify_from_title
from apps.seo.base import BaseSEO
from apps.common.upload_utils import listing_image_upload_to


class Listing(BaseSEO, models.Model):
    # =====================================================
    # Enums
    # =====================================================
    class Deal(models.TextChoices):
        BUY = "buy", "فروش"
        RENT = "rent", "اجاره"

    class Status(models.TextChoices):
        DRAFT = "draft", "پیش‌نویس"
        PUBLISHED = "published", "منتشر شده"
        ARCHIVED = "archived", "بایگانی شده"

    # =====================================================
    # Core Identity
    # =====================================================
    title = models.CharField(max_length=255, verbose_name="عنوان")
    slug = models.SlugField(max_length=255, blank=True, db_index=True, verbose_name="اسلاگ")

    # =====================================================
    # Location & Category (Search backbone)
    # =====================================================
    city = models.ForeignKey(
        "locations.City",
        on_delete=models.PROTECT,
        related_name="listings",
        verbose_name="شهر",
    )

    area = models.ForeignKey(
        "locations.Area",
        on_delete=models.PROTECT,
        related_name="listings",
        null=True,
        blank=True,
        verbose_name="محله",
    )

    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.PROTECT,
        related_name="listings",
        verbose_name="دسته‌بندی",
    )

    # =====================================================
    # Deal & Lifecycle
    # =====================================================
    deal = models.CharField(
        max_length=10,
        choices=Deal.choices,
        default=Deal.BUY,
        db_index=True,
        verbose_name="نوع معامله",
    )

    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
        verbose_name="وضعیت",
    )

    published_at = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ انتشار")

    # =====================================================
    # Content (Human-readable)
    # =====================================================
    short_description = models.TextField(
        blank=True,
        verbose_name="خلاصه کوتاه",
        help_text="خلاصه برای meta و کارت آگهی",
    )

    description = RichTextField(
        blank=True,
        verbose_name="توضیحات",
        help_text="محتوای اصلی آگهی",
    )

    # =====================================================
    # Optional Pricing (generic – not opinionated)
    # =====================================================
    price = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name="قیمت",
        help_text="قیمت اصلی (خرید یا اجاره)",
    )

    price_unit = models.CharField(
        max_length=32,
        blank=True,
        verbose_name="واحد قیمت",
        help_text="مثال: تومان، دلار، متر",
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
        verbose_name="ایجادکننده",
    )
    agency = models.ForeignKey(
        "agencies.Agency",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="listings",
        verbose_name="مشاوره املاک",
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
        verbose_name = "آگهی"
        verbose_name_plural = "آگهی‌ها"
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
            self.slug = slugify_from_title(self.title)

        # Auto publish timestamp
        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        if self.slug:
            return f"/l/{self.id}-{self.slug}/"
        return f"/l/{self.id}/"



class ListingImage(models.Model):
    listing = models.ForeignKey(
        "listings.Listing",
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="آگهی",
    )

    image = models.ImageField(upload_to=listing_image_upload_to, verbose_name="تصویر")
    alt = models.CharField(max_length=180, blank=True, verbose_name="متن جایگزین")

    sort_order = models.PositiveIntegerField(default=0, verbose_name="ترتیب")
    is_cover = models.BooleanField(default=False, verbose_name="تصویر شاخص")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "تصویر آگهی"
        verbose_name_plural = "تصاویر آگهی"
        ordering = ("sort_order", "id")
        indexes = [
            models.Index(fields=["listing", "sort_order"]),
            models.Index(fields=["listing", "is_cover"]),
        ]

    def __str__(self):
        return f"تصویر {self.id} برای آگهی {self.listing_id}"
