def panel_neshan_api_key(request):
    """کلید API نقشه نشان برای صفحات پنل."""
    if "/panel" not in request.path:
        return {}
    import os
    from django.conf import settings

    key = getattr(settings, "NESHAN_API_KEY", None) or os.environ.get("NESHAN_API_KEY", "") or ""
    return {"neshan_api_key": key}


def panel_pending_count(request):
    """شمارنده‌های پنل: تاییدهای ادمین و دعوت‌های همکاری کاربر."""
    if "/panel" not in request.path:
        return {}
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return {}

    from apps.agencies.models import AgencyEmployeeInvite

    ctx = {
        "pending_invites_count": AgencyEmployeeInvite.objects.filter(
            invited_user=user,
            status=AgencyEmployeeInvite.Status.PENDING,
        ).count()
    }

    if user.is_superuser or user.groups.filter(name="site_admin").exists():
        from apps.listings.models import Listing
        from apps.agencies.models import Agency

        pending_listings = Listing.objects.filter(status=Listing.Status.PENDING).count()
        pending_agencies = Agency.objects.filter(
            approval_status=Agency.ApprovalStatus.PENDING
        ).count()
        ctx["pending_approve_count"] = pending_listings + pending_agencies

    return ctx
