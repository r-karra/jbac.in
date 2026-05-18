from django.urls import path

from .views import churches_api, news_api, pastors_api, platform_stats_api
from .api_views import (
	meetings_api,
	meeting_detail_api,
	jobs_api,
	job_detail_api,
	businesses_api,
	institutes_api,
	incidents_api,
	gallery_categories_api,
	gallery_images_api,
	prayers_api,
	leaders_api,
	marriages_api,
	news_api as news_api_v2,
	lookups_districts_api,
	lookups_states_api,
	lookups_meeting_types_api,
	lookups_job_types_api,
	lookups_business_types_api,
	lookups_incident_types_api,
	lookups_prayer_categories_api,
	lookups_job_categories_api,
	lookups_business_categories_api,
	lookups_institute_types_api,
	lookups_institute_categories_api,
)

app_name = "api"

urlpatterns = [
	# Stats
	path("stats/", platform_stats_api, name="stats"),
	
	# Directory
	path("pastors/", pastors_api, name="pastors"),
	path("churches/", churches_api, name="churches"),
	
	# Meetings/Events
	path("meetings/", meetings_api, name="meetings"),
	path("meetings/<int:meeting_id>/", meeting_detail_api, name="meeting_detail"),
	
	# Jobs
	path("jobs/", jobs_api, name="jobs"),
	path("jobs/<int:job_id>/", job_detail_api, name="job_detail"),
	
	# Businesses
	path("businesses/", businesses_api, name="businesses"),
	
	# Institutes
	path("institutes/", institutes_api, name="institutes"),
	
	# Incidents
	path("incidents/", incidents_api, name="incidents"),
	
	# Gallery
	path("gallery/categories/", gallery_categories_api, name="gallery_categories"),
	path("gallery/images/<int:category_id>/", gallery_images_api, name="gallery_images"),
	
	# Prayers
	path("prayers/", prayers_api, name="prayers"),
	
	# Leaders
	path("leaders/", leaders_api, name="leaders"),
	
	# Marriages
	path("marriages/", marriages_api, name="marriages"),
	
	# News (using v2)
	path("news/", news_api_v2, name="news"),
	
	# Lookups/Reference Data
	path("lookups/districts/", lookups_districts_api, name="lookups_districts"),
	path("lookups/states/", lookups_states_api, name="lookups_states"),
	path("lookups/meeting-types/", lookups_meeting_types_api, name="lookups_meeting_types"),
	path("lookups/job-types/", lookups_job_types_api, name="lookups_job_types"),
	path("lookups/business-types/", lookups_business_types_api, name="lookups_business_types"),
	path("lookups/incident-types/", lookups_incident_types_api, name="lookups_incident_types"),
	path("lookups/prayer-categories/", lookups_prayer_categories_api, name="lookups_prayer_categories"),
	path("lookups/job-categories/", lookups_job_categories_api, name="lookups_job_categories"),
	path("lookups/business-categories/", lookups_business_categories_api, name="lookups_business_categories"),
	path("lookups/institute-types/", lookups_institute_types_api, name="lookups_institute_types"),
	path("lookups/institute-categories/", lookups_institute_categories_api, name="lookups_institute_categories"),
]