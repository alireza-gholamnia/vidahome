"""
سیگنال‌ها برای حساب کاربری.
"""
from django.contrib.auth.models import Group
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import User


@receiver(post_save, sender=User)
def assign_member_role_to_new_user(sender, instance, created, **kwargs):
    """هر کاربر جدید هنگام ایجاد، نقش member را دریافت می‌کند (اگر هیچ نقشی ندارد)."""
    if not created:
        return
    if instance.groups.exists():
        return
    member_grp, _ = Group.objects.get_or_create(name="member")
    instance.groups.add(member_grp)


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
