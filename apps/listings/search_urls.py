from django.urls import path
from django.views.generic import RedirectView

from .views import (
    s_one_segment,
    city_context,
    area_category,
)

app_name = "search"

urlpatterns = [
    path("", RedirectView.as_view(url="/listings/", permanent=True), name="listing_catalog"),
    path("<slug:slug>/", s_one_segment, name="s_one_segment"),
    path("<slug:city_slug>/<slug:context_slug>/", city_context, name="city_context"),
    path("<slug:city_slug>/<slug:area_slug>/<slug:category_slug>/", area_category, name="area_category"),
]
