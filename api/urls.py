from django.urls import path

from .views import churches_api, news_api, pastors_api, platform_stats_api

app_name = "api"

urlpatterns = [
	path("stats/", platform_stats_api, name="stats"),
	path("pastors/", pastors_api, name="pastors"),
	path("churches/", churches_api, name="churches"),
	path("news/", news_api, name="news"),
]