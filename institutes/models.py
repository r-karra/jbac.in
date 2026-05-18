from django.db import models
from django.conf import settings
from directory.models import DISTRICT_CHOICES, STATE_CHOICES, ApprovalFields


INSTITUTE_TYPE_CHOICES = [
	("college", "College"),
	("university", "University"),
	("school", "School"),
	("training-center", "Training Center"),
	("seminary", "Theological Seminary"),
	("vocational", "Vocational Institute"),
	("coaching", "Coaching Center"),
	("other", "Other"),
]

DEGREE_LEVEL_CHOICES = [
	("high-school", "High School"),
	("diploma", "Diploma"),
	("bachelor", "Bachelor's"),
	("master", "Master's"),
	("phd", "PhD"),
	("certificate", "Certificate"),
	("other", "Other"),
]


class InstituteCategory(models.Model):
	name = models.CharField(max_length=100, unique=True)
	description = models.TextField(blank=True)

	class Meta:
		verbose_name_plural = "Institute Categories"
		ordering = ["name"]

	def __str__(self):
		return self.name


class Institute(ApprovalFields):
	posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posted_institutes")
	institute_name = models.CharField(max_length=200)
	description = models.TextField()
	institute_type = models.CharField(max_length=30, choices=INSTITUTE_TYPE_CHOICES)
	category = models.ForeignKey(InstituteCategory, on_delete=models.SET_NULL, null=True, blank=True)
	
	district = models.CharField(max_length=100, choices=DISTRICT_CHOICES)
	state = models.CharField(max_length=100, choices=STATE_CHOICES, default="Andhra Pradesh")
	city_area = models.CharField(max_length=100, blank=True)
	address = models.TextField()
	
	latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
	longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
	
	principal_name = models.CharField(max_length=200, blank=True)
	principal_email = models.EmailField(blank=True)
	principal_phone = models.CharField(max_length=20, blank=True)
	
	website = models.URLField(blank=True)
	established_year = models.PositiveIntegerField(blank=True, null=True)
	student_count = models.PositiveIntegerField(blank=True, null=True)
	
	degrees_offered = models.CharField(max_length=200, help_text="Comma-separated degrees offered")
	specializations = models.TextField(blank=True, help_text="Available specializations")
	
	image_url = models.URLField(blank=True)
	affiliation = models.CharField(max_length=200, blank=True, help_text="University/Board affiliation")
	
	posted_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-posted_date"]

	def __str__(self):
		return self.institute_name
