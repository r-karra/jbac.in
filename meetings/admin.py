from django.contrib import admin
from django.contrib import messages

from .models import Meeting


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
	list_display = (
		"title",
		"start_date",
		"end_date",
		"district",
		"organizer_name",
		"is_published",
		"updated_at",
	)
	list_filter = ("is_published", "district", "meeting_type", "denomination", "ministry")
	search_fields = ("title", "description", "organizer_name", "address", "city_area", "mandal", "village")
	ordering = ("start_date", "title")
	actions = ("mark_as_published", "mark_as_unpublished")

	@admin.action(description="Publish selected meetings")
	def mark_as_published(self, request, queryset):
		updated = queryset.update(is_published=True)
		self.message_user(request, f"Published {updated} meeting(s).", level=messages.SUCCESS)

	@admin.action(description="Unpublish selected meetings")
	def mark_as_unpublished(self, request, queryset):
		updated = queryset.update(is_published=False)
		self.message_user(request, f"Unpublished {updated} meeting(s).", level=messages.WARNING)
