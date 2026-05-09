from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField

from apps.common.text_utils import slugify_from_title
from apps.common.upload_utils import service_provider_image_upload_to, service_provider_logo_upload_to
from apps.seo.base import BaseSEO


class ServiceProvider(BaseSEO, models.Model):
    """شرکت یا شخص ارائه‌دهنده سرویس‌های مرتبط با ملک."""

    class ProviderType(models.TextChoices):
        COMPANY = "company", "شرکت"
        PERSON = "person", "شخص"

    class ApprovalStatus(models.TextChoices):
        PENDING = "pending", "در انتظار تأیید"
        APPROVED = "approved", "تأیید شده"
        REJECTED = "rejected", "رد شده"

    name = models.CharField(max_length=180, verbose_name="نام")
    slug = models.SlugField(max_length=200, db_index=True, unique=True, blank=True, verbose_name="اسلاگ")
    provider_type = models.CharField(
        max_length=12,
        choices=ProviderType.choices,
        default=ProviderType.COMPANY,
        db_index=True,
        verbose_name="نوع ارائه‌دهنده",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="service_providers",
        verbose_name="کاربر مالک",
    )
    categories = models.ManyToManyField(
        "categories.Category",
        related_name="service_providers",
        limit_choices_to={"category_type": "service"},
        verbose_name="دسته‌های سرویس",
    )
    cities = models.ManyToManyField(
        "locations.City",
        related_name="service_providers",
        blank=True,
        verbose_name="شهرهای تحت پوشش",
    )
    approval_status = models.CharField(
        max_length=12,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.PENDING,
        db_index=True,
        verbose_name="وضعیت تأیید",
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="تلفن")
    mobile = models.CharField(max_length=20, blank=True, verbose_name="موبایل")
    email = models.EmailField(blank=True, verbose_name="ایمیل")
    website = models.URLField(blank=True, verbose_name="وب‌سایت")
    address = models.TextField(blank=True, verbose_name="آدرس")
    intro_content = models.TextField(blank=True, verbose_name="متن معرفی")
    main_content = RichTextUploadingField(blank=True, verbose_name="محتوای اصلی")
    logo = models.ImageField(
        upload_to=service_provider_logo_upload_to,
        blank=True,
        null=True,
        verbose_name="لوگو/تصویر پروفایل",
    )
    is_active = models.BooleanField(default=True, db_index=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")

    class Meta:
        verbose_name = "ارائه‌دهنده سرویس"
        verbose_name_plural = "ارائه‌دهندگان سرویس"
        ordering = ("name", "id")

    def __str__(self):
        return self.name

    def clean(self):
        if self.website and not self.website.startswith(("http://", "https://")):
            raise ValidationError({"website": "آدرس وب‌سایت باید با http:// یا https:// شروع شود."})

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify_from_title(self.name, max_length=200)
            candidate = base_slug
            suffix = 2
            while ServiceProvider.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                suffix_text = f"-{suffix}"
                candidate = f"{base_slug[: 200 - len(suffix_text)]}{suffix_text}"
                suffix += 1
            self.slug = candidate
        self.full_clean(exclude=["categories", "cities"])
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/services/p/{self.id}-{self.slug}/"

    def get_landing_cover_image(self):
        images = list(self.images.all())
        for image in images:
            if image.is_landing_cover:
                return image
        return images[0] if images else None


class ServiceProviderImage(models.Model):
    """گالری تصاویر ارائه‌دهنده سرویس."""

    provider = models.ForeignKey(
        ServiceProvider,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="ارائه‌دهنده",
    )
    image = models.ImageField(upload_to=service_provider_image_upload_to, verbose_name="تصویر")
    alt = models.CharField(max_length=180, blank=True, verbose_name="متن جایگزین")
    caption = models.CharField(max_length=200, blank=True, verbose_name="عنوان")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="ترتیب")
    is_cover = models.BooleanField(default=False, verbose_name="تصویر شاخص")
    is_landing_cover = models.BooleanField(default=False, verbose_name="کاور لندینگ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        ordering = ("sort_order", "id")
        verbose_name = "تصویر ارائه‌دهنده سرویس"
        verbose_name_plural = "تصاویر ارائه‌دهندگان سرویس"

    def __str__(self):
        return f"Image {self.id} for {self.provider.name}"
