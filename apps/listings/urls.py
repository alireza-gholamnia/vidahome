from django.urls import path
from django.views.generic import RedirectView
from .views import city_landing

urlpatterns = [
    path(
        "",
        RedirectView.as_view(url="/", permanent=False),
        name="search_root_redirect",
    ),
    path(
        "<slug:city_slug>/",
        city_landing,
        name="city_landing",
    ),
]
