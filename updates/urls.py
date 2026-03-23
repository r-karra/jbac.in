from django.urls import path

from .views import news_detail, news_list, submit_news

app_name = "updates"

urlpatterns = [
    path("", news_list, name="list"),
    path("submit/", submit_news, name="submit"),
    path("<slug:slug>/", news_detail, name="detail"),
]