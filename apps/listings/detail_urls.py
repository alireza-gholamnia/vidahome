from django.urls import path
from . import views

app_name = "listings"


urlpatterns = [
    # canonical form
    path("<int:listing_id>-<slug:slug>/", views.listing_detail, name="detail"),
    # id-only form
    path("<int:listing_id>/", views.listing_detail_by_id, name="detail_by_id"),
]