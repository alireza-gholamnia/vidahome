"""
همگام‌سازی ویژگی‌های آگهی با دسته‌بندی.
وقتی دسته‌بندی آگهی مشخص است، رکوردهای ListingAttribute برای تمام ویژگی‌های
آن دسته ایجاد می‌شوند (با مقدار خالی) و ویژگی‌های نامرتبط حذف می‌شوند.
فقط ویژگی‌هایی که حداقل یک دسته‌بندی دارند نمایش داده می‌شوند.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.attributes.models import Attribute, ListingAttribute

from .models import Listing


def sync_listing_attributes(listing):
    """
    همگام‌سازی ویژگی‌های آگهی با دسته‌بندی.
    - ویژگی‌های بدون دسته‌بندی نمایش داده نمی‌شوند
    - برای هر ویژگی مربوط به دسته، اگر رکورد وجود نداشت ایجاد می‌کند
    - رکوردهای ویژگی‌های نامرتبط را حذف می‌کند
    """
    if not listing.pk:
        return
    if not listing.category_id:
        ListingAttribute.objects.filter(listing=listing).delete()
        return

    # فقط ویژگی‌های مربوط به این دسته (ویژگی بدون دسته نمایش داده نمی‌شود)
    category_attrs = Attribute.objects.filter(
        categories=listing.category,
        is_active=True,
    ).order_by("sort_order", "id").distinct()

    valid_attr_ids = set(category_attrs.values_list("id", flat=True))

    # حذف ویژگی‌های نامرتبط
    ListingAttribute.objects.filter(listing=listing).exclude(
        attribute_id__in=valid_attr_ids
    ).delete()

    # ایجاد رکوردهای جدید برای ویژگی‌هایی که هنوز وجود ندارند
    existing_attr_ids = set(
        ListingAttribute.objects.filter(listing=listing).values_list(
            "attribute_id", flat=True
        )
    )
    for attr in category_attrs:
        if attr.id not in existing_attr_ids:
            ListingAttribute.objects.create(
                listing=listing,
                attribute=attr,
            )


@receiver(post_save, sender=Listing)
def listing_post_save_sync_attributes(sender, instance, created, **kwargs):
    sync_listing_attributes(instance)
