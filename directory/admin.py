from django.contrib import admin

from .models import BelieverProfile, ChurchProfile, OrganizationProfile, PastorProfile, StudentProfile, Leader, Marriage


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


@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
	list_display = ("name", "role", "district", "organization_name", "is_approved", "posted_date")
	list_filter = ("role", "district", "is_approved", "posted_date")
	search_fields = ("name", "organization_name", "email", "phone")
	readonly_fields = ("posted_date", "created_at", "updated_at")
	fieldsets = (
		(
			"Leader Details",
			{
				"fields": ("name", "role", "organization_name")
			},
		),
		(
			"Location",
			{
				"fields": ("district", "state")
			},
		),
		(
			"Contact",
			{
				"fields": ("email", "phone")
			},
		),
		(
			"Ministry",
			{
				"fields": ("years_in_ministry", "biography")
			},
		),
		(
			"Media",
			{
				"fields": ("image_url",)
			},
		),
		(
			"Meta",
			{
				"fields": ("user", "is_approved", "is_public", "posted_date", "created_at", "updated_at")
			},
		),
	)


@admin.register(Marriage)
class MarriageAdmin(admin.ModelAdmin):
	list_display = ("name", "gender", "district", "marital_status", "is_approved", "posted_date")
	list_filter = ("gender", "marital_status", "district", "is_approved", "posted_date")
	search_fields = ("name", "email", "phone", "district")
	readonly_fields = ("posted_date", "created_at", "updated_at")
	fieldsets = (
		(
			"Personal Details",
			{
				"fields": ("name", "gender", "date_of_birth", "marital_status")
			},
		),
		(
			"Location",
			{
				"fields": ("district", "state")
			},
		),
		(
			"Contact",
			{
				"fields": ("email", "phone", "phone_visible")
			},
		),
		(
			"Professional & Educational",
			{
				"fields": ("occupation", "education")
			},
		),
		(
			"About Me",
			{
				"fields": ("about_me", "interests", "looking_for")
			},
		),
		(
			"Media",
			{
				"fields": ("image_url",)
			},
		),
		(
			"Meta",
			{
				"fields": ("submitted_by", "is_approved", "is_public", "posted_date", "created_at", "updated_at")
			},
		),
	)
