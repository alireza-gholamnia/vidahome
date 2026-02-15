from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.blog_index, name="index"),
    path("category/<slug:slug>/", views.blog_category, name="category"),
    path("<slug:slug>/", views.blog_post_detail, name="detail"),
]
