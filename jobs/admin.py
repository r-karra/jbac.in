from django.contrib import admin
from .models import JobCategory, Job, JobApplication


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
	list_display = ["name", "icon"]
	search_fields = ["name"]


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
	list_display = ["title", "company_name", "job_type", "district", "is_approved", "created_at"]
	list_filter = ["job_type", "experience_level", "is_approved", "is_public", "district", "created_at"]
	search_fields = ["title", "company_name", "description", "district"]
	readonly_fields = ["created_at", "posted_date"]
	fieldsets = (
		("Job Details", {
			"fields": ("title", "description", "category", "job_type", "experience_level", "education_level")
		}),
		("Location & Salary", {
			"fields": ("district", "state", "city_area", "salary_min", "salary_max", "currency")
		}),
		("Company", {
			"fields": ("company_name", "company_email", "company_phone", "company_website")
		}),
		("Requirements", {
			"fields": ("skills_required", "benefits", "deadline")
		}),
		("Application", {
			"fields": ("application_link", "application_email")
		}),
		("Meta", {
			"fields": ("posted_by", "is_approved", "is_public", "created_at", "posted_date")
		}),
	)


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
	list_display = ["applicant", "job", "status", "applied_at"]
	list_filter = ["status", "applied_at"]
	search_fields = ["job__title", "applicant__email"]
	readonly_fields = ["applied_at", "updated_at"]
