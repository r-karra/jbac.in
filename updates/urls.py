from django.urls import path

from .views import news_detail, news_list

app_name = "updates"

urlpatterns = [
    path("", news_list, name="list"),
    path("<slug:slug>/", news_detail, name="detail"),
]