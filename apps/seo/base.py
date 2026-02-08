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
        help_text="Optional SEO title override"
    )

    seo_meta_description = models.TextField(
        blank=True,
        help_text="Optional meta description override"
    )

    seo_h1 = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional H1 override"
    )

    seo_canonical = models.URLField(
        blank=True,
        help_text="Optional canonical URL"
    )

    seo_noindex = models.BooleanField(
        default=False,
        help_text="Force noindex for this page"
    )

    allow_index = models.BooleanField(
        default=True,
        help_text="If false, page will be noindex regardless of other rules"
    )

    seo_priority = models.PositiveSmallIntegerField(
        default=5,
        help_text="SEO priority for sitemap / crawl budget (1-10)"
    )

    class Meta:
        abstract = True

