from django.contrib import admin
from .models import BusinessCategory, Business


@admin.register(BusinessCategory)
class BusinessCategoryAdmin(admin.ModelAdmin):
	list_display = ["name", "icon"]
	search_fields = ["name"]


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
	list_display = ["business_name", "business_type", "district", "owner_name", "is_approved", "posted_date"]
	list_filter = ["business_type", "is_approved", "is_public", "district", "posted_date"]
	search_fields = ["business_name", "description", "owner_name", "district"]
	readonly_fields = ["posted_date", "created_at", "updated_at"]
	fieldsets = (
		("Business Details", {
			"fields": ("business_name", "description", "category", "business_type")
		}),
		("Location", {
			"fields": ("district", "state", "city_area", "address", "latitude", "longitude")
		}),
		("Owner Information", {
			"fields": ("owner_name", "owner_email", "owner_phone")
		}),
		("Additional Info", {
			"fields": ("website", "established_year", "logo_url", "image_url", "services_offered", "working_hours")
		}),
		("Meta", {
			"fields": ("posted_by", "is_approved", "is_public", "posted_date", "created_at", "updated_at")
		}),
	)
