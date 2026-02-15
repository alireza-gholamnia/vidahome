from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from ckeditor_uploader.fields import RichTextUploadingField

from apps.seo.base import BaseSEO
from apps.common.text_utils import slugify_from_title
from apps.common.upload_utils import blog_cover_upload_to


class BlogCategory(models.Model):
    """دسته‌بندی داخلی بلاگ — مستقل از دسته‌بندی ملک."""

    fa_name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, db_index=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("sort_order", "id")
        verbose_name = "دسته‌بندی بلاگ"
        verbose_name_plural = "دسته‌بندی‌های بلاگ"

    def __str__(self):
        return self.fa_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.fa_name) or "blog-cat"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/blog/category/{self.slug}/"


class BlogPost(BaseSEO, models.Model):
    """پست بلاگ — با امکان ارتباط با لندینگ‌های پروژه."""

    class Status(models.TextChoices):
        DRAFT = "draft", "پیش‌نویس"
        PUBLISHED = "published", "منتشر شده"

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    excerpt = models.TextField(blank=True, help_text="خلاصه کوتاه برای کارت و meta")
    content = RichTextUploadingField(blank=True)
    cover_image = models.ImageField(
        upload_to=blog_cover_upload_to,
        blank=True,
        null=True,
    )
    published_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blog_posts",
    )
    blog_category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )

    # ارتباط با لندینگ‌های پروژه
    city = models.ForeignKey(
        "locations.City",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blog_posts",
    )
    area = models.ForeignKey(
        "locations.Area",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blog_posts",
    )
    listing_category = models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blog_posts",
        verbose_name="دسته‌بندی ملک",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-published_at", "-id")
        verbose_name = "پست بلاگ"
        verbose_name_plural = "پست‌های بلاگ"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify_from_title(self.title)
            slug = base
            c = 1
            qs = BlogPost.objects if self.pk else BlogPost.objects.all()
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            while qs.filter(slug=slug).exists():
                slug = f"{base}-{c}"
                c += 1
            self.slug = slug
        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/blog/{self.slug}/"

    def get_landing_links(self):
        """لینک‌های مرتبط به لندینگ‌ها برای نمایش در پست."""
        links = []
        if self.city:
            links.append({"title": self.city.fa_name, "url": self.city.get_absolute_url()})
        if self.area:
            links.append({"title": f"{self.area.fa_name} ({self.area.city.fa_name})", "url": self.area.get_absolute_url()})
        if self.listing_category:
            links.append({"title": self.listing_category.fa_name, "url": self.listing_category.get_absolute_url()})
        if self.city and self.listing_category:
            links.append({
                "title": f"{self.listing_category.fa_name} در {self.city.fa_name}",
                "url": f"/s/{self.city.slug}/{self.listing_category.slug}/",
            })
        return links
