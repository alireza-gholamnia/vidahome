from django.contrib.auth.models import Group
from django.db.models import Q
from django.utils import timezone


BUSINESS_GROUPS = ("member", "agency_owner", "agency_employee")


def _get_or_create_group(name: str) -> Group:
    group, _ = Group.objects.get_or_create(name=name)
    return group


def set_exclusive_business_role(user, role_name: str) -> None:
    """
    Set exactly one business role for user among:
    member / agency_owner / agency_employee.
    """
    if role_name not in BUSINESS_GROUPS:
        raise ValueError(f"Invalid business role: {role_name}")

    current_groups = list(user.groups.filter(name__in=BUSINESS_GROUPS))
    if current_groups:
        user.groups.remove(*current_groups)
    user.groups.add(_get_or_create_group(role_name))


def user_owns_any_agency(user, *, approved_only: bool = False) -> bool:
    from apps.agencies.models import AgencyMembership

    return get_user_agencies_for_roles(
        user,
        roles=(AgencyMembership.Role.OWNER,),
        approved_only=approved_only,
    ).exists()


def get_user_agencies_for_roles(user, *, roles, approved_only: bool = False):
    """Return agencies where user has one of the active membership roles."""
    from apps.agencies.models import Agency, AgencyMembership

    if not user or not getattr(user, "is_authenticated", False):
        return Agency.objects.none()

    membership_agency_ids = AgencyMembership.objects.filter(
        user=user,
        status=AgencyMembership.Status.ACTIVE,
        role__in=roles,
    ).values_list("agency_id", flat=True)
    filters = Q(id__in=membership_agency_ids)

    if AgencyMembership.Role.OWNER in roles:
        filters |= Q(owner=user)

    staff_roles = {AgencyMembership.Role.MANAGER, AgencyMembership.Role.EMPLOYEE}
    if staff_roles.intersection(set(roles)) and getattr(user, "agency_id", None):
        filters |= Q(id=user.agency_id)

    qs = Agency.objects.filter(filters).distinct()
    if approved_only:
        qs = qs.filter(
            is_active=True,
            approval_status=Agency.ApprovalStatus.APPROVED,
        )
    return qs


def assign_user_to_agency(user, agency) -> None:
    """Assign user to agency and enforce employee role."""
    from apps.agencies.models import AgencyMembership

    now = timezone.now()
    AgencyMembership.objects.filter(
        user=user,
        status=AgencyMembership.Status.ACTIVE,
        role__in=(AgencyMembership.Role.MANAGER, AgencyMembership.Role.EMPLOYEE),
    ).exclude(agency=agency).update(status=AgencyMembership.Status.LEFT, left_at=now)

    if user.agency_id != agency.id:
        user.agency = agency
        user.save(update_fields=["agency"])
    AgencyMembership.objects.update_or_create(
        user=user,
        agency=agency,
        role=AgencyMembership.Role.EMPLOYEE,
        defaults={
            "status": AgencyMembership.Status.ACTIVE,
            "left_at": None,
        },
    )
    set_exclusive_business_role(user, "agency_employee")


def clear_user_agency_membership(user, agency=None) -> None:
    """
    Remove user from agency and normalize role:
    - owner if user owns any agency
    - member otherwise
    """
    from apps.agencies.models import AgencyMembership

    now = timezone.now()
    memberships = AgencyMembership.objects.filter(
        user=user,
        status=AgencyMembership.Status.ACTIVE,
        role__in=(AgencyMembership.Role.MANAGER, AgencyMembership.Role.EMPLOYEE),
    )
    if agency is not None:
        memberships = memberships.filter(agency=agency)
    memberships.update(status=AgencyMembership.Status.LEFT, left_at=now)

    should_clear_legacy_agency = (
        user.agency_id is not None
        and (agency is None or user.agency_id == agency.id)
    )
    if should_clear_legacy_agency:
        user.agency = None
        user.save(update_fields=["agency"])

    if user_owns_any_agency(user, approved_only=False):
        set_exclusive_business_role(user, "agency_owner")
    else:
        set_exclusive_business_role(user, "member")


def promote_user_to_owner(user) -> None:
    """Promote user to agency_owner and clear agency employee membership."""
    clear_user_agency_membership(user)
    set_exclusive_business_role(user, "agency_owner")
