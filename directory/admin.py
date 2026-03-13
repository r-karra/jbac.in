from django.contrib import admin

from .models import BelieverProfile, ChurchProfile, OrganizationProfile, PastorProfile, StudentProfile


@admin.register(BelieverProfile)
class BelieverProfileAdmin(admin.ModelAdmin):
	list_display = ("full_name", "user", "is_approved", "is_public", "created_at")
	list_filter = ("is_approved", "is_public", "created_at")
	search_fields = ("full_name", "user__mobile_number", "user__email")


@admin.register(PastorProfile)
class PastorProfileAdmin(admin.ModelAdmin):
	list_display = ("pastor_name", "church_name", "district", "state", "is_approved", "is_public")
	list_filter = ("district", "state", "is_approved", "is_public")
	search_fields = ("pastor_name", "church_name", "user__mobile_number", "user__email")


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
	list_display = ("student_name", "college_name", "district", "state", "is_approved")
	list_filter = ("district", "state", "is_approved")
	search_fields = ("student_name", "college_name", "user__mobile_number", "user__email")


@admin.register(ChurchProfile)
class ChurchProfileAdmin(admin.ModelAdmin):
	list_display = ("church_name", "pastor_name", "district", "state", "is_approved", "is_public")
	list_filter = ("district", "state", "is_approved", "is_public")
	search_fields = ("church_name", "pastor_name", "user__mobile_number", "user__email")


@admin.register(OrganizationProfile)
class OrganizationProfileAdmin(admin.ModelAdmin):
	list_display = ("organization_name", "founder_name", "district", "state", "is_approved", "is_public")
	list_filter = ("district", "state", "is_approved", "is_public")
	search_fields = ("organization_name", "founder_name", "user__mobile_number", "user__email")
