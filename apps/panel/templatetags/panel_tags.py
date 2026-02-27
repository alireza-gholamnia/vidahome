from django import template
from django.contrib.auth import get_user_model

User = get_user_model()
register = template.Library()


@register.filter
def has_agency(user):
    """آیا کاربر حداقل یک املاک فعال و تاییدشده دارد؟"""
    if not user or not user.is_authenticated:
        return False
    from apps.agencies.models import Agency
    return Agency.objects.filter(
        owner=user,
        is_active=True,
        approval_status=Agency.ApprovalStatus.APPROVED,
    ).exists()


@register.filter
def is_agency_owner(user):
    """آیا کاربر مالک حداقل یک املاک است؟"""
    if not user or not user.is_authenticated:
        return False
    from apps.agencies.models import Agency

    return Agency.objects.filter(
        owner=user,
        is_active=True,
        approval_status=Agency.ApprovalStatus.APPROVED,
    ).exists()


@register.filter
def is_agency_employee(user):
    """آیا کاربر در حال حاضر عضو یک املاک است؟"""
    if not user or not user.is_authenticated:
        return False
    return bool(getattr(user, "agency_id", None))


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
    from apps.agencies.models import Agency
    if not listing.agency_id:
        return False

    approved_active = {
        "approval_status": Agency.ApprovalStatus.APPROVED,
        "is_active": True,
    }
    if Agency.objects.filter(owner=user, id=listing.agency_id, **approved_active).exists():
        return True
    return Agency.objects.filter(
        id=listing.agency_id,
        **approved_active,
    ).exists() and bool(getattr(user, "agency_id", None) == listing.agency_id)


def _can_delete(user, listing):
    return _can_edit(user, listing)


@register.filter
def can_edit_listing(user, listing):
    return _can_edit(user, listing)


@register.filter
def can_delete_listing(user, listing):
    return _can_delete(user, listing)
