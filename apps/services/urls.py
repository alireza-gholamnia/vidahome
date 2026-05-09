from django.urls import path

from . import views

app_name = "services"

urlpatterns = [
    path("", views.service_directory, name="directory"),
    path("providers/", views.service_provider_list, name="provider_list"),
    path("p/<int:provider_id>-<slug:slug>/", views.service_provider_detail, name="provider_detail"),
    path("p/<int:provider_id>/", views.service_provider_detail_by_id, name="provider_detail_by_id"),
    path("<slug:slug>/", views.service_category, name="category"),
]
