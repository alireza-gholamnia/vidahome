from django import template
from django.contrib.auth import get_user_model

User = get_user_model()
register = template.Library()


@register.filter
def has_agency(user):
    """آیا کاربر صاحب یک مشاوره املاک است؟"""
    if not user or not user.is_authenticated:
        return False
    from apps.agencies.models import Agency
    return Agency.objects.filter(owner=user).exists()


@register.filter
def is_agency_owner(user):
    """آیا کاربر در گروه صاحب مشاوره است؟"""
    if not user or not user.is_authenticated:
        return False
    return user.groups.filter(name="agency_owner").exists()


@register.filter
def is_agency_employee(user):
    """آیا کاربر در گروه کارمند مشاوره است؟"""
    if not user or not user.is_authenticated:
        return False
    return user.groups.filter(name="agency_employee").exists()


@register.filter
def is_agent(user):
    """آیا کاربر صاحب یا کارمند مشاوره است و لندینگ دارد؟"""
    if not user:
        return False
    return getattr(user, "is_agent", lambda: False)()


@register.filter
def is_site_admin(user):
    """آیا کاربر ادمین سایت است (سوپرادمین یا گروه site_admin)؟"""
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name="site_admin").exists()


def _can_edit(user, listing):
    if not user or not user.is_authenticated or not listing:
        return False
    if user.is_superuser:
        return True
    if listing.created_by_id == user.id:
        return True
    from apps.agencies.models import Agency
    if listing.agency_id and Agency.objects.filter(owner=user, id=listing.agency_id).exists():
        return True
    return False


def _can_delete(user, listing):
    return _can_edit(user, listing)


@register.filter
def can_edit_listing(user, listing):
    return _can_edit(user, listing)


@register.filter
def can_delete_listing(user, listing):
    return _can_delete(user, listing)
