from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import OTPChallenge, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
	ordering = ("mobile_number",)
	list_display = ("member_id", "mobile_number", "email", "role", "is_staff", "is_active")
	search_fields = ("mobile_number", "email", "first_name", "last_name")

	fieldsets = (
		(None, {"fields": ("mobile_number", "password")}),
		(
			"Personal info",
			{"fields": ("member_id", "first_name", "last_name", "email", "role", "preferred_language")},
		),
		(
			"Permissions",
			{
				"fields": (
					"is_active",
					"is_staff",
					"is_superuser",
					"groups",
					"user_permissions",
				)
			},
		),
		("Important dates", {"fields": ("last_login", "date_joined")}),
	)

	add_fieldsets = (
		(
			None,
			{
				"classes": ("wide",),
				"fields": ("mobile_number", "role", "email", "password1", "password2"),
			},
		),
	)


@admin.register(OTPChallenge)
class OTPChallengeAdmin(admin.ModelAdmin):
	list_display = (
		"user",
		"role",
		"identifier",
		"request_ip",
		"failed_attempts",
		"locked_until",
		"expires_at",
		"is_used",
		"created_at",
	)
	list_filter = ("role", "is_used", "created_at", "locked_until")
	search_fields = ("user__mobile_number", "user__email", "identifier", "code")
