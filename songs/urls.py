from django.urls import path

from .views import books_list, song_detail, songs_search

app_name = "songs"

urlpatterns = [
    path("", songs_search, name="search"),
    path("books/", books_list, name="books"),
    path("view/", song_detail, name="detail"),
    path("<slug:category>/", songs_search, name="category"),
]
