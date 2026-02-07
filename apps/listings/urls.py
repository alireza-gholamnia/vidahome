from django.urls import path
from django.views.generic import RedirectView

from .views import (
    s_root_redirect,      # /s
    s_one_segment,        # /s/{slug}  -> City OR Category
    city_context,         # /s/{city}/{category} OR /s/{city}/{area}
    area_category,        # /s/{city}/{area}/{category}
)

urlpatterns = [
    # ---------------------------------------------------------
    # /s
    # Search namespace only → redirect to home
    # ---------------------------------------------------------
    path("", s_root_redirect, name="search_root_redirect"),

    # ---------------------------------------------------------
    # /s/{slug}
    # Example:
    #   /s/lahijan  -> City landing
    #   /s/zamin    -> Category landing
    # ---------------------------------------------------------
    path("<slug:slug>/", s_one_segment, name="s_one_segment"),

    # ---------------------------------------------------------
    # /s/{city}/{category}
    # /s/{city}/{area}
    # Example:
    #   /s/lahijan/zamin        -> City + Category landing
    #   /s/lahijan/sheikh-zahed -> City + Area landing
    # ---------------------------------------------------------
    path("<slug:city_slug>/<slug:context_slug>/", city_context, name="city_context"),

    # ---------------------------------------------------------
    # /s/{city}/{area}/{category}
    # Example: /s/lahijan/sheikh-zahed/zamin
    # ---------------------------------------------------------
    path("<slug:city_slug>/<slug:area_slug>/<slug:category_slug>/", area_category, name="area_category"),
]
