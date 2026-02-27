from django.contrib.auth.models import Group


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
    from apps.agencies.models import Agency

    qs = user.owned_agencies.all()
    if approved_only:
        qs = qs.filter(
            is_active=True,
            approval_status=Agency.ApprovalStatus.APPROVED,
        )
    return qs.exists()


def assign_user_to_agency(user, agency) -> None:
    """Assign user to agency and enforce employee role."""
    if user.agency_id != agency.id:
        user.agency = agency
        user.save(update_fields=["agency"])
    set_exclusive_business_role(user, "agency_employee")


def clear_user_agency_membership(user) -> None:
    """
    Remove user from agency and normalize role:
    - owner if user owns any agency
    - member otherwise
    """
    if user.agency_id is not None:
        user.agency = None
        user.save(update_fields=["agency"])

    if user_owns_any_agency(user, approved_only=False):
        set_exclusive_business_role(user, "agency_owner")
    else:
        set_exclusive_business_role(user, "member")


def promote_user_to_owner(user) -> None:
    """Promote user to agency_owner and clear agency employee membership."""
    if user.agency_id is not None:
        user.agency = None
        user.save(update_fields=["agency"])
    set_exclusive_business_role(user, "agency_owner")
