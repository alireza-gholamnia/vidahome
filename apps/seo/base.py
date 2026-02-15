from django.db import models

# =====================================================
# Base SEO (abstract)
# =====================================================

class BaseSEO(models.Model):
    """
    Base SEO fields shared by City and Area.
    This model ONLY handles SEO concerns.
    """

    seo_title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="عنوان سئو",
        help_text="عنوان جایگزین برای سئو",
    )

    seo_meta_description = models.TextField(
        blank=True,
        verbose_name="توضیحات متا",
        help_text="توضیحات جایگزین meta description",
    )

    seo_h1 = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="عنوان H1",
        help_text="عنوان H1 جایگزین",
    )

    seo_canonical = models.URLField(
        blank=True,
        verbose_name="آدرس کانونیکال",
        help_text="URL کانونیکال",
    )

    seo_noindex = models.BooleanField(
        default=False,
        verbose_name="بدون ایندکس",
        help_text="عدم ایندکس شدن صفحه",
    )

    allow_index = models.BooleanField(
        default=True,
        verbose_name="مجوز ایندکس",
        help_text="در صورت غیرفعال، صفحه ایندکس نمی‌شود",
    )

    seo_priority = models.PositiveSmallIntegerField(
        default=5,
        verbose_name="اولویت سئو",
        help_text="اولویت برای sitemap (۱ تا ۱۰)",
    )

    class Meta:
        abstract = True

