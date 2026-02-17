from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "accounts"

urlpatterns = [
    path("", RedirectView.as_view(url="/accounts/login/", permanent=False)),
    path("login/", views.PhoneLoginView.as_view(), name="login"),
    path("login/verify/", views.OTPVerifyView.as_view(), name="otp_verify"),
    path("api/request-otp/", views.RequestOtpApiView.as_view(), name="api_request_otp"),
    path("api/verify-otp/", views.VerifyOtpApiView.as_view(), name="api_verify_otp"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
]
