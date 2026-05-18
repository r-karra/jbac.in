from django.db import models
from django.conf import settings
from directory.models import DISTRICT_CHOICES, STATE_CHOICES, ApprovalFields


BUSINESS_TYPE_CHOICES = [
	("retail", "Retail"),
	("food-beverage", "Food & Beverage"),
	("service", "Service"),
	("manufacturing", "Manufacturing"),
	("it-software", "IT & Software"),
	("healthcare", "Healthcare"),
	("education", "Education"),
	("real-estate", "Real Estate"),
	("finance", "Finance"),
	("agriculture", "Agriculture"),
	("transportation", "Transportation"),
	("other", "Other"),
]


class BusinessCategory(models.Model):
	name = models.CharField(max_length=100, unique=True)
	description = models.TextField(blank=True)
	icon = models.CharField(max_length=50, blank=True)

	class Meta:
		verbose_name_plural = "Business Categories"
		ordering = ["name"]

	def __str__(self):
		return self.name


class Business(ApprovalFields):
	posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posted_businesses")
	business_name = models.CharField(max_length=200)
	description = models.TextField()
	category = models.ForeignKey(BusinessCategory, on_delete=models.SET_NULL, null=True, blank=True)
	business_type = models.CharField(max_length=50, choices=BUSINESS_TYPE_CHOICES)
	
	district = models.CharField(max_length=100, choices=DISTRICT_CHOICES)
	state = models.CharField(max_length=100, choices=STATE_CHOICES, default="Andhra Pradesh")
	city_area = models.CharField(max_length=100, blank=True)
	address = models.TextField()
	
	latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
	longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
	
	owner_name = models.CharField(max_length=200)
	owner_email = models.EmailField()
	owner_phone = models.CharField(max_length=20)
	
	website = models.URLField(blank=True)
	established_year = models.PositiveIntegerField(blank=True, null=True)
	
	logo_url = models.URLField(blank=True)
	image_url = models.URLField(blank=True)
	
	services_offered = models.TextField(blank=True)
	working_hours = models.CharField(max_length=100, blank=True)
	
	posted_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-posted_date"]

	def __str__(self):
		return self.business_name
