from django.urls import path

from .views import about, about_subpage, admin_dashboard, contact, dashboard, home

app_name = "core"

urlpatterns = [
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("about-us/", about_subpage, name="about-us"),
    path("about-us/<slug:section>/", about_subpage, name="about-section"),
    path("contact/", contact, name="contact"),
    path("dashboard/", dashboard, name="dashboard"),
    path("admin-dashboard/", admin_dashboard, name="admin-dashboard"),
]