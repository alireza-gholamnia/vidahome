"""
سیگنال‌ها برای حساب کاربری.
"""
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import User


@receiver(pre_save, sender=User)
def transfer_listings_on_agency_change(sender, instance, **kwargs):
    """
    وقتی مشاوره املاک کاربر (کارمند) عوض می‌شود، آگهی‌های او
    در مشاوره قبلی به صاحب آن مشاوره منتقل می‌شوند.
    """
    if not instance.pk:
        return  # کاربر جدید
    try:
        old_user = User.objects.get(pk=instance.pk)
    except User.DoesNotExist:
        return
    old_agency_id = old_user.agency_id
    new_agency_id = instance.agency_id
    if old_agency_id == new_agency_id:
        return  # مشاوره تغییری نکرده
    if not old_agency_id:
        return  # قبلاً مشاوره‌ای نداشت
    from apps.listings.models import Listing

    old_agency = old_user.agency
    if not old_agency or not old_agency.owner_id:
        return
    Listing.objects.filter(
        created_by_id=instance.pk,
        agency_id=old_agency_id,
    ).update(created_by_id=old_agency.owner_id)
