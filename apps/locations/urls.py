from django.urls import path
from .views import cities_directory

urlpatterns = [
    path("", cities_directory, name="cities_directory"),
]
