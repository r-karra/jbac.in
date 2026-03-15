from django.urls import path

from .views import song_detail, songs_search

app_name = "songs"

urlpatterns = [
    path("", songs_search, name="search"),
    path("view/", song_detail, name="detail"),
    path("<slug:category>/", songs_search, name="category"),
]
