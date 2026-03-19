from django.urls import path

from .views import (
    about,
    about_subpage,
    admin_dashboard,
    contact,
    dashboard,
    home,
    privacy_policy,
    terms_conditions,
)

app_name = "core"

urlpatterns = [
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("about-us/", about_subpage, name="about-us"),
    path("about-us/<slug:section>/", about_subpage, name="about-section"),
    path("contact/", contact, name="contact"),
    path("privacy-policy/", privacy_policy, name="privacy-policy"),
    path("terms-and-conditions/", terms_conditions, name="terms-and-conditions"),
    path("dashboard/", dashboard, name="dashboard"),
    path("admin-dashboard/", admin_dashboard, name="admin-dashboard"),
]