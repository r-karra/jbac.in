from django.urls import path

from .views import LoginView, OTPRequestView, OTPVerifyView, logout_view

app_name = "accounts"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("otp/", OTPRequestView.as_view(), name="otp-request"),
    path("otp/verify/", OTPVerifyView.as_view(), name="otp-verify"),
    path("logout/", logout_view, name="logout"),
]