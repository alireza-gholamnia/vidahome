from django.db import models
from django.conf import settings

from ckeditor_uploader.fields import RichTextUploadingField
from apps.seo.base import BaseSEO
from apps.common.upload_utils import agency_logo_upload_to, agency_image_upload_to
from apps.common.text_utils import slugify_from_title


class Agency(BaseSEO, models.Model):
    """
    مشاوره املاک — دارای لندینگ اختصاصی /a/{id}-{slug}/
    """
    name = models.CharField(max_length=180, verbose_name="نام")
    slug = models.SlugField(max_length=200, db_index=True, unique=True, blank=True, verbose_name="اسلاگ")
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_agency",
        verbose_name="مالک",
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="تلفن")
    address = models.TextField(blank=True, verbose_name="آدرس")
    intro_content = models.TextField(blank=True, verbose_name="متن معرفی")
    main_content = RichTextUploadingField(blank=True, verbose_name="محتوای اصلی")
    logo = models.ImageField(upload_to=agency_logo_upload_to, blank=True, null=True, verbose_name="لوگو")
    cities = models.ManyToManyField(
        "locations.City",
        related_name="agencies",
        blank=True,
        verbose_name="شهرها",
    )
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "مشاوره املاک"
        verbose_name_plural = "مشاوره‌های املاک"
        ordering = ("name",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_from_title(self.name, max_length=200)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/a/{self.id}-{self.slug}/"

    def get_landing_cover_image(self):
        images = list(self.images.all())
        for img in images:
            if img.is_landing_cover:
                return img
        return images[0] if images else None


class AgencyImage(models.Model):
    """گالری تصاویر مشاوره املاک."""
    agency = models.ForeignKey(
        Agency,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="مشاوره املاک",
    )
    image = models.ImageField(upload_to=agency_image_upload_to, verbose_name="تصویر")
    alt = models.CharField(max_length=180, blank=True, verbose_name="متن جایگزین")
    caption = models.CharField(max_length=200, blank=True, verbose_name="عنوان")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="ترتیب")
    is_cover = models.BooleanField(default=False, verbose_name="تصویر شاخص")
    is_landing_cover = models.BooleanField(default=False, verbose_name="کاور لندینگ")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("sort_order", "id")
        verbose_name = "تصویر مشاوره"
        verbose_name_plural = "تصاویر مشاوره"

    def __str__(self):
        return f"Image {self.id} for {self.agency.name}"
