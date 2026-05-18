from django.contrib import admin
from .models import Incident


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
	list_display = ["title", "incident_type", "severity", "status", "district", "incident_date"]
	list_filter = ["incident_type", "severity", "status", "district", "incident_date"]
	search_fields = ["title", "description", "victim_name", "police_station", "district"]
	readonly_fields = ["report_date", "updated_at", "created_at"]
	fieldsets = (
		("Incident Details", {
			"fields": ("title", "description", "incident_type", "severity", "status")
		}),
		("Timeline", {
			"fields": ("incident_date", "report_date", "updated_at")
		}),
		("Location", {
			"fields": ("district", "state", "location", "latitude", "longitude")
		}),
		("Victim Information", {
			"fields": ("victim_name", "victim_phone", "victim_email", "witnesses")
		}),
		("Legal Information", {
			"fields": ("fir_number", "police_station", "evidence_attachments")
		}),
		("Resolution", {
			"fields": ("resolution_notes",)
		}),
		("Meta", {
			"fields": ("reported_by", "is_approved", "is_public", "created_at")
		}),
	)
