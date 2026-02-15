from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.apps import apps

from apps.seo.base import BaseSEO
from ckeditor_uploader.fields import RichTextUploadingField
from apps.common.upload_utils import category_image_upload_to


class Category(BaseSEO, models.Model):
    """
    Category with parent/child hierarchy.
    Slug is globally unique to keep URL paths unambiguous.
    """

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="children",
        verbose_name="دسته والد",
        help_text="دسته والد (ساختار درختی)",
    )

    fa_name = models.CharField(max_length=120, verbose_name="نام فارسی")
    en_name = models.CharField(max_length=120, verbose_name="نام انگلیسی")

    slug = models.SlugField(max_length=140, db_index=True, verbose_name="اسلاگ")

    is_active = models.BooleanField(default=True, verbose_name="فعال")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="ترتیب")

    # --- Landing content ---
    intro_content = models.TextField(blank=True, verbose_name="متن معرفی")
    main_content = RichTextUploadingField(
        blank=True,
        verbose_name="محتوای اصلی",
        help_text="محتوا با امکان درج و آپلود تصویر",
    )

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ("sort_order", "id")
        constraints = [
            models.UniqueConstraint(fields=["slug"], name="uniq_category_slug"),
            models.UniqueConstraint(fields=["en_name"], name="uniq_category_en_name"),
            models.CheckConstraint(
                condition=~models.Q(id=models.F("parent_id")),
                name="category_parent_not_self",
            ),
        ]

    def __str__(self):
        return self.fa_name

    @property
    def is_root(self):
        return self.parent_id is None

    def clean(self):
        # --- 1) Prevent Category.slug collision with City slugs ---
        City = apps.get_model("locations", "City")
        if self.slug and City.objects.filter(slug=self.slug).exists():
            raise ValidationError({"slug": "This slug is reserved for an existing city."})

        # --- 2) Prevent cycles in category tree ---
        ancestor = self.parent
        while ancestor is not None:
            if self.pk and ancestor.pk == self.pk:
                raise ValidationError({"parent": "Invalid parent: cyclic category hierarchy."})
            ancestor = ancestor.parent

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.en_name)
        self.full_clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/s/{self.slug}/"

    def get_cover_image(self):
        """تصویر شاخص برای کارت دسته‌بندی."""
        images = list(self.images.all())
        for img in images:
            if img.is_cover:
                return img
        return images[0] if images else None

    def get_landing_cover_image(self):
        """تصویر کاور صفحه لندینگ دسته‌بندی."""
        images = list(self.images.all())
        for img in images:
            if img.is_landing_cover:
                return img
        return images[0] if images else None


# =====================================================
# CategoryImage
# =====================================================

class CategoryImage(models.Model):
    """
    گالری تصاویر دسته‌بندی.
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to=category_image_upload_to)
    alt = models.CharField(max_length=180, blank=True)
    caption = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_cover = models.BooleanField(default=False, help_text="تصویر کارت دسته‌بندی")
    is_landing_cover = models.BooleanField(default=False, help_text="کاور صفحه لندینگ")
    is_content_image = models.BooleanField(default=False, help_text="تصاویر محتوا")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("sort_order", "id")
        verbose_name = "تصویر دسته‌بندی"
        verbose_name_plural = "تصاویر دسته‌بندی"

    def __str__(self):
        return f"Image {self.id} for {self.category.fa_name}"
