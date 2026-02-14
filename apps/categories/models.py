from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.apps import apps

from apps.seo.base import BaseSEO
from ckeditor.fields import RichTextField


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
        help_text="Optional parent category (tree structure)."
    )

    fa_name = models.CharField(max_length=120)
    en_name = models.CharField(max_length=120)

    slug = models.SlugField(max_length=140, db_index=True)

    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    # --- Landing content ---
    intro_content = models.TextField(blank=True)
    main_content = RichTextField(blank=True)

    class Meta:
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
