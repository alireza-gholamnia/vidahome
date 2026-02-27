from django.urls import path

from . import views

app_name = "panel"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("listings/", views.ListingListView.as_view(), name="listing_list"),
    path("listings/add/", views.ListingCreateView.as_view(), name="listing_add"),
    path("listings/<int:pk>/edit/", views.ListingUpdateView.as_view(), name="listing_edit"),
    path("listings/<int:pk>/delete/", views.ListingDeleteView.as_view(), name="listing_delete"),
    path("listings/inquiries/", views.listing_inquiries, name="listing_inquiries"),
    path("profile/", views.profile_edit, name="profile_edit"),
    path("agencies/", views.agency_list, name="agency_list"),
    path("agencies/add/", views.agency_add, name="agency_add"),
    path("agencies/<int:pk>/edit/", views.agency_edit, name="agency_edit"),
    path("employee/request-join/", views.employee_request_join, name="employee_request_join"),
    path("employee/my-agency/", views.employee_my_agency, name="employee_my_agency"),
    path("agency/employees/", views.agency_employees, name="agency_employees"),
    path("approve/", views.approve_dashboard, name="approve_dashboard"),
    path("approve/listing/<int:pk>/", views.approve_listing, name="approve_listing"),
    path("approve/agency/<int:pk>/", views.approve_agency, name="approve_agency"),
    path("approve/employee/<int:user_id>/manage/", views.employee_manage_agency, name="employee_manage_agency"),
    path("attributes/", views.attribute_list, name="attribute_list"),
    path("attributes/add/", views.attribute_add, name="attribute_add"),
    path("attributes/<int:pk>/edit/", views.attribute_edit, name="attribute_edit"),
    path("attributes/<int:pk>/delete/", views.attribute_delete, name="attribute_delete"),
    path("api/reverse-geocode/", views.reverse_geocode_json, name="reverse_geocode_json"),
    path("api/areas/", views.areas_json, name="areas_json"),
    path("api/attributes/", views.attributes_json, name="attributes_json"),
]
