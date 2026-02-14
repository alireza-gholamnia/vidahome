from django.db import models
from django.utils.text import slugify
from django.conf import settings

from ckeditor_uploader.fields import RichTextUploadingField
from apps.seo.base import BaseSEO
from apps.common.upload_utils import agency_logo_upload_to, agency_image_upload_to


class Agency(BaseSEO, models.Model):
    """
    مشاوره املاک — دارای لندینگ اختصاصی /a/{slug}/
    """
    name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_agency",
    )
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    intro_content = models.TextField(blank=True)
    main_content = RichTextUploadingField(blank=True)
    logo = models.ImageField(upload_to=agency_logo_upload_to, blank=True, null=True)
    cities = models.ManyToManyField(
        "locations.City",
        related_name="agencies",
        blank=True,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "مشاوره املاک"
        verbose_name_plural = "مشاوره‌های املاک"
        ordering = ("name",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/a/{self.slug}/"

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
    )
    image = models.ImageField(upload_to=agency_image_upload_to)
    alt = models.CharField(max_length=180, blank=True)
    caption = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_cover = models.BooleanField(default=False)
    is_landing_cover = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("sort_order", "id")
        verbose_name = "تصویر مشاوره"
        verbose_name_plural = "تصاویر مشاوره"

    def __str__(self):
        return f"Image {self.id} for {self.agency.name}"
