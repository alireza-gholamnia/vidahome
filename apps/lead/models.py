"""مدل‌های لید — استعلام‌ها و فرم‌های تماس از صفحات مختلف."""
from django.db import models


class LeadStatus(models.TextChoices):
    """وضعیت مشترک لیدها."""
    NEW = "new", "جدید"
    VIEWED = "viewed", "مشاهده شده"
    CONTACTED = "contacted", "تماس گرفته شده"


class ListingLead(models.Model):
    """لید از صفحه جزئیات آگهی."""
    LeadStatus = LeadStatus  # برای دسترسی از خارج (مثل ListingLead.LeadStatus)
    listing = models.ForeignKey(
        "listings.Listing",
        on_delete=models.CASCADE,
        related_name="leads",
        verbose_name="آگهی",
    )
    first_name = models.CharField(max_length=60, verbose_name="نام", blank=True)
    last_name = models.CharField(max_length=60, verbose_name="نام خانوادگی", blank=True)
    name = models.CharField(max_length=120, verbose_name="نام کامل", blank=True, help_text="نام + نام خانوادگی؛ برای نمایش و جستجو")
    phone = models.CharField(max_length=20, verbose_name="تلفن")
    message = models.TextField(blank=True, verbose_name="پیام")
    status = models.CharField(
        max_length=12,
        choices=LeadStatus.choices,
        default=LeadStatus.NEW,
        db_index=True,
        verbose_name="وضعیت",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ")

    class Meta:
        verbose_name = "لید آگهی"
        verbose_name_plural = "لیدهای آگهی"
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        # همیشه نام کامل را از نام و نام خانوادگی بساز (برای نمایش و جستجو)
        self.name = f"{self.first_name or ''} {self.last_name or ''}".strip()
        super().save(*args, **kwargs)

    def __str__(self):
        display = self.name or f"{self.first_name or ''} {self.last_name or ''}".strip() or "-"
        return f"{display} — آگهی {self.listing_id}"

    def get_source_display(self):
        """صفحه مبدا: جزئیات آگهی."""
        return f"آگهی: {self.listing.title}"


class LandingLead(models.Model):
    """لید از لندینگ‌ها (شهر، دسته، شهر+دسته، تماس، و غیره)."""

    class SourceType(models.TextChoices):
        CITY = "city", "لندینگ شهر"
        CATEGORY = "category", "لندینگ دسته"
        AREA = "area", "لندینگ محله"
        CITY_CATEGORY = "city_category", "لندینگ شهر+دسته"
        AREA_CATEGORY = "area_category", "لندینگ محله+دسته"
        CONTACT = "contact", "صفحه تماس با ما"
        OTHER = "other", "سایر"

    source_type = models.CharField(
        max_length=20,
        choices=SourceType.choices,
        db_index=True,
        verbose_name="نوع صفحه",
    )
    source_path = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="مسیر صفحه",
        help_text="مثال: tehran، apartment، tehran/apartment",
    )
    name = models.CharField(max_length=120, verbose_name="نام")
    phone = models.CharField(max_length=20, verbose_name="تلفن")
    email = models.EmailField(blank=True, verbose_name="ایمیل")
    subject = models.CharField(max_length=200, blank=True, verbose_name="موضوع")
    message = models.TextField(blank=True, verbose_name="پیام")
    status = models.CharField(
        max_length=12,
        choices=LeadStatus.choices,
        default=LeadStatus.NEW,
        db_index=True,
        verbose_name="وضعیت",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ")

    class Meta:
        verbose_name = "لید لندینگ"
        verbose_name_plural = "لیدهای لندینگ"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name} — {self.get_source_type_display()}"

    def get_source_display(self):
        """نمایش صفحه مبدا برای ادمین."""
        if self.source_path:
            return f"{self.get_source_type_display()} ({self.source_path})"
        return self.get_source_type_display()
