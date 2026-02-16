"""URLهای لندینگ مشاورین املاک — /agent/"""
from django.shortcuts import redirect
from django.urls import path
from . import views

app_name = "agents"


def _redirect_agent_by_id(request, user_id):
    return redirect("agents:landing_by_id", user_id=user_id, permanent=False)


urlpatterns = [
    path("<int:user_id>-<slug:slug>/", views.agent_landing, name="landing"),
    path("<int:user_id>-/", _redirect_agent_by_id, name="landing_slug_empty"),
    path("<int:user_id>/", views.agent_landing_by_id, name="landing_by_id"),
]
