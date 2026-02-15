from django.shortcuts import redirect
from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "agencies"


def _redirect_agency_by_id(request, agency_id):
    return redirect("agencies:landing_by_id", agency_id=agency_id, permanent=False)


urlpatterns = [
    path("", RedirectView.as_view(url="/agencies/", permanent=True)),
    path("<int:agency_id>-<slug:slug>/", views.agency_landing, name="landing"),
    path("<int:agency_id>/", views.agency_landing_by_id, name="landing_by_id"),
    path("<int:agency_id>-/", _redirect_agency_by_id),
    path("<str:slug>/", views.agency_landing_by_slug, name="landing_by_slug"),
]
