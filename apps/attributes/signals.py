"""
وقتی مقداری جدید در ویژگی آگهی وارد شود، در جدول گزینه‌های ویژگی هم ثبت می‌شود
تا برای انتخاب‌های بعدی در دسترس باشد.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import AttributeOption, ListingAttribute


@receiver(post_save, sender=ListingAttribute)
def listing_attribute_sync_to_options(sender, instance, **kwargs):
    """
    وقتی مقدار در ListingAttribute ذخیره شد، اگر در AttributeOption وجود نداشت، اضافه کن.
    """
    if not instance.attribute_id:
        return
    attr = instance.attribute
    if instance.value_int is not None:
        val = str(instance.value_int)
        AttributeOption.objects.get_or_create(
            attribute=attr,
            value=val,
            defaults={"sort_order": instance.value_int},
        )
    elif instance.value_str:
        AttributeOption.objects.get_or_create(
            attribute=attr,
            value=instance.value_str,
            defaults={"sort_order": 0},
        )
