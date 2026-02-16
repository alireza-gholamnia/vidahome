from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "accounts"

urlpatterns = [
    path("", RedirectView.as_view(url="/accounts/login/", permanent=False)),
    path("login/", views.PhoneLoginView.as_view(), name="login"),
    path("login/verify/", views.OTPVerifyView.as_view(), name="otp_verify"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
]
