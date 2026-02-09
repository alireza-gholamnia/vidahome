from django.urls import path

from .views import (
    s_root_redirect,
    s_one_segment,
    city_context,
    area_category,
)

app_name = "search"

urlpatterns = [
    path("", s_root_redirect, name="search_root_redirect"),
    path("<slug:slug>/", s_one_segment, name="s_one_segment"),
    path("<slug:city_slug>/<slug:context_slug>/", city_context, name="city_context"),
    path("<slug:city_slug>/<slug:area_slug>/<slug:category_slug>/", area_category, name="area_category"),
]
