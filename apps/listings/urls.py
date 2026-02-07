from django.urls import path
from django.views.generic import RedirectView
from .views import city_landing, area_landing

urlpatterns = [
    path("", RedirectView.as_view(url="/", permanent=False), name="search_root_redirect"),
    path("<slug:city_slug>/", city_landing, name="city_landing"),
    path("<slug:city_slug>/<slug:area_slug>/", area_landing, name="area_landing"),
]
