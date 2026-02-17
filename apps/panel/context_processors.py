def panel_neshan_api_key(request):
    """کلید API نقشه نشان برای صفحات پنل."""
    if "/panel" not in request.path:
        return {}
    import os
    from django.conf import settings
    key = getattr(settings, "NESHAN_API_KEY", None) or os.environ.get("NESHAN_API_KEY", "") or ""
    return {"neshan_api_key": key}


def panel_pending_count(request):
    """تعداد موارد در انتظار تأیید برای ادمین سایت در پنل."""
    if "/panel" not in request.path:
        return {}
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return {}
    if not user.is_superuser and not user.groups.filter(name="site_admin").exists():
        return {}
    from apps.listings.models import Listing
    from apps.agencies.models import Agency

    from apps.agencies.models import AgencyJoinRequest

    pending_listings = Listing.objects.filter(status=Listing.Status.PENDING).count()
    pending_agencies = Agency.objects.filter(
        approval_status=Agency.ApprovalStatus.PENDING
    ).count()
    pending_join_requests = AgencyJoinRequest.objects.filter(
        status=AgencyJoinRequest.Status.PENDING
    ).count()
    return {
        "pending_approve_count": pending_listings
        + pending_agencies
        + pending_join_requests
    }
