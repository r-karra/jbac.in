from django.urls import path

from .views import submit_meeting, view_meetings

app_name = "meetings"

urlpatterns = [
	path("submit/", submit_meeting, name="submit"),
	path("view/", view_meetings, name="view"),
]
