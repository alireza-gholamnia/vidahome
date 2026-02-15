from django.shortcuts import redirect
from django.urls import path
from . import views

app_name = "listings"


def _redirect_to_listing_by_id(request, listing_id):
    return redirect("listings:detail_by_id", listing_id=listing_id, permanent=False)


urlpatterns = [
    # canonical form (slug must be non-empty)
    path("<int:listing_id>-<slug:slug>/", views.listing_detail, name="detail"),
    # id-only form
    path("<int:listing_id>/", views.listing_detail_by_id, name="detail_by_id"),
    # fallback: id- (empty slug) -> redirect to id-only
    path("<int:listing_id>-/", _redirect_to_listing_by_id),
]