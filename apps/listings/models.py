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
        DAILY_RENT = "daily_rent", "اجاره روزانه"
        MORTGAGE_RENT = "mortgage_rent", "رهن و اجاره"

    class Status(models.TextChoices):
        DRAFT = "draft", "پیش‌نویس"
        PENDING = "pending", "در انتظار تأیید"
        PUBLISHED = "published", "منتشر شده"
        REJECTED = "rejected", "رد شده"
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

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True,
        verbose_name="عرض جغرافیایی",
        help_text="انتخاب روی نقشه هنگام ثبت آگهی",
    )
    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True,
        verbose_name="طول جغرافیایی",
        help_text="انتخاب روی نقشه هنگام ثبت آگهی",
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
        max_length=16,
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

    rejection_reason = models.TextField(
        blank=True,
        verbose_name="علت رد",
        help_text="توضیح ادمین هنگام رد آگهی؛ به صاحب آگهی نمایش داده می‌شود.",
    )

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
    # Optional Pricing (deal-dependent)
    # =====================================================
    price = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name="قیمت",
        help_text="قیمت اصلی (خرید / اجاره ماهانه / اجاره روزانه / اجاره ماهانه در رهن‌واجاره)",
    )

    price_mortgage = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name="مبلغ رهن",
        help_text="فقط برای نوع «رهن و اجاره»",
    )

    price_unit = models.CharField(
        max_length=32,
        blank=True,
        verbose_name="واحد قیمت",
        help_text="مثال: تومان، دلار، تومان/روز",
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

    def get_deal_display_fa(self):
        """برگرداندن برچسب فارسی نوع معامله."""
        return dict(self.Deal.choices).get(self.deal, self.deal)

    def has_price_display(self):
        """آیا این آگهی حداقل یک قیمت برای نمایش دارد؟"""
        if self.deal == self.Deal.MORTGAGE_RENT:
            return bool(self.price is not None or self.price_mortgage is not None)
        return self.price is not None

    def get_pending_type_display(self):
        """نوع آگهی در صف تأیید برای نمایش به ادمین."""
        if self.status != self.Status.PENDING:
            return ""
        if self.rejection_reason:
            return "ارسال مجدد پس از رد"
        if self.published_at:
            return "ویرایش شده در انتظار تأیید"
        return "ثبت شده در انتظار تأیید"



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
