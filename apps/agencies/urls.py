from django.urls import path
from . import views

app_name = "agencies"

urlpatterns = [
    path("<slug:slug>/", views.agency_landing, name="landing"),
]
