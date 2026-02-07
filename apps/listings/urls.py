from django.urls import path
from django.views.generic import RedirectView

from .views import (
    category_landing,   # /s/{category}
    city_landing,       # /s/{city}
    city_context,       # /s/{city}/{category} OR /s/{city}/{area}
    area_category,      # /s/{city}/{area}/{category}
)

urlpatterns = [
    # ---------------------------------------------------------
    # /s
    # Search namespace only → NO PAGE → redirect to home
    # ---------------------------------------------------------
    path(
        "",
        RedirectView.as_view(url="/", permanent=False),
        name="search_root_redirect",
    ),

    # ---------------------------------------------------------
    # /s/{category}
    # Example: /s/apartment
    # ---------------------------------------------------------
    path(
        "<slug:category_slug>/",
        category_landing,
        name="category_landing",
    ),

    # ---------------------------------------------------------
    # /s/{city}
    # Example: /s/rasht
    # ---------------------------------------------------------
    path(
        "<slug:city_slug>/",
        city_landing,
        name="city_landing",
    ),

    # ---------------------------------------------------------
    # /s/{city}/{category}
    # /s/{city}/{area}
    #
    # Example:
    #   /s/rasht/apartment   → City + Category landing
    #   /s/rasht/golsar     → City + Area landing
    #
    # Resolver: city_context
    # ---------------------------------------------------------
    path(
        "<slug:city_slug>/<slug:context_slug>/",
        city_context,
        name="city_context",
    ),

    # ---------------------------------------------------------
    # /s/{city}/{area}/{category}
    # Example: /s/rasht/golsar/apartment
    # ---------------------------------------------------------
    path(
        "<slug:city_slug>/<slug:area_slug>/<slug:category_slug>/",
        area_category,
        name="area_category",
    ),
]
