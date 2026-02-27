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

    class CategoryType(models.TextChoices):
        PROPERTY = "property", "نوع ملک"
        PROJECT = "project", "پروژه"
        SERVICE = "service", "سرویس"
        CONTENT_TAG = "content_tag", "تگ محتوایی"

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="children",
        verbose_name="دسته والد",
        help_text="دسته والد (ساختار درختی)",
    )

    category_type = models.CharField(
        max_length=24,
        choices=CategoryType.choices,
        default=CategoryType.PROPERTY,
        db_index=True,
        verbose_name="نوع دسته‌بندی",
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

    @classmethod
    def property_queryset(cls):
        return cls.objects.filter(category_type=cls.CategoryType.PROPERTY)

    @classmethod
    def listing_type_values(cls):
        return (
            cls.CategoryType.PROPERTY,
            cls.CategoryType.PROJECT,
            cls.CategoryType.SERVICE,
        )

    @classmethod
    def landing_type_values(cls):
        return cls.listing_type_values()

    @classmethod
    def listing_queryset(cls):
        return cls.objects.filter(category_type__in=cls.listing_type_values())

    @classmethod
    def landing_queryset(cls):
        return cls.objects.filter(category_type__in=cls.landing_type_values())

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

        # Keep trees type-consistent.
        if self.parent and self.parent.category_type != self.category_type:
            raise ValidationError({"parent": "Parent category must have the same type."})

        # Prevent breaking listing/search landings by switching an in-use category to a non-supported type.
        if self.pk and self.listings.exists() and self.category_type not in self.listing_type_values():
            raise ValidationError({
                "category_type": "This category is used by listings and must stay as property/project/service."
            })
        if self.pk and (self.seo_city_categories.exists() or self.seo_area_categories.exists()):
            if self.category_type not in self.landing_type_values():
                raise ValidationError({
                    "category_type": "This category is used by city/area landings and must stay as property/project/service."
                })

        # Prevent parent/child type mismatch when changing current category type.
        if self.pk and self.children.exclude(category_type=self.category_type).exists():
            raise ValidationError({
                "category_type": "All child categories must have the same type as parent."
            })

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
