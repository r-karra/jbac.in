from django.db import models
from django.conf import settings
from directory.models import DISTRICT_CHOICES, STATE_CHOICES, ApprovalFields


INCIDENT_TYPE_CHOICES = [
	("harassment", "Harassment"),
	("violence", "Violence"),
	("discrimination", "Discrimination"),
	("persecution", "Persecution"),
	("property-damage", "Property Damage"),
	("fraud", "Fraud"),
	("threat", "Threat"),
	("other", "Other"),
]

SEVERITY_CHOICES = [
	("low", "Low"),
	("medium", "Medium"),
	("high", "High"),
	("critical", "Critical"),
]

STATUS_CHOICES = [
	("reported", "Reported"),
	("under-review", "Under Review"),
	("investigating", "Investigating"),
	("resolved", "Resolved"),
	("closed", "Closed"),
]


class Incident(ApprovalFields):
	reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="reported_incidents")
	title = models.CharField(max_length=200)
	description = models.TextField()
	incident_type = models.CharField(max_length=30, choices=INCIDENT_TYPE_CHOICES)
	severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default="medium")
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="reported")
	
	incident_date = models.DateTimeField()
	report_date = models.DateTimeField(auto_now_add=True)
	
	district = models.CharField(max_length=100, choices=DISTRICT_CHOICES)
	state = models.CharField(max_length=100, choices=STATE_CHOICES, default="Andhra Pradesh")
	location = models.CharField(max_length=200)
	
	latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
	longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
	
	victim_name = models.CharField(max_length=200, blank=True)
	victim_phone = models.CharField(max_length=20, blank=True)
	victim_email = models.EmailField(blank=True)
	
	witnesses = models.TextField(blank=True, help_text="Comma-separated witness names or contact info")
	
	fir_number = models.CharField(max_length=100, blank=True, help_text="First Information Report number if filed")
	police_station = models.CharField(max_length=200, blank=True)
	
	evidence_attachments = models.TextField(blank=True, help_text="URLs to attached documents/images")
	
	resolution_notes = models.TextField(blank=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-incident_date"]

	def __str__(self):
		return f"{self.title} - {self.get_severity_display()}"
