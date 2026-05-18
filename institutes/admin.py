from django.contrib import admin
from .models import InstituteCategory, Institute


@admin.register(InstituteCategory)
class InstituteCategoryAdmin(admin.ModelAdmin):
	list_display = ["name"]
	search_fields = ["name"]


@admin.register(Institute)
class InstituteAdmin(admin.ModelAdmin):
	list_display = ["institute_name", "institute_type", "district", "principal_name", "is_approved", "posted_date"]
	list_filter = ["institute_type", "is_approved", "is_public", "district", "posted_date"]
	search_fields = ["institute_name", "description", "principal_name", "district"]
	readonly_fields = ["posted_date", "created_at", "updated_at"]
	fieldsets = (
		("Institute Details", {
			"fields": ("institute_name", "description", "institute_type", "category")
		}),
		("Location", {
			"fields": ("district", "state", "city_area", "address", "latitude", "longitude")
		}),
		("Leadership", {
			"fields": ("principal_name", "principal_email", "principal_phone")
		}),
		("Academic Information", {
			"fields": ("website", "established_year", "student_count", "degrees_offered", "specializations", "affiliation")
		}),
		("Media", {
			"fields": ("image_url",)
		}),
		("Meta", {
			"fields": ("posted_by", "is_approved", "is_public", "posted_date", "created_at", "updated_at")
		}),
	)
