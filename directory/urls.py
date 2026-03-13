from django.urls import path

from .views import map_search, member_id_pdf, register_category, registration_landing, search_directory

app_name = "directory"

urlpatterns = [
    path("register/", registration_landing, name="register"),
    path("register/<slug:category>/", register_category, name="register-category"),
    path("search/", search_directory, name="search"),
    path("map-search/", map_search, name="map-search"),
    path("member-id/", member_id_pdf, name="member-id"),
]