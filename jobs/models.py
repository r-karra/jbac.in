from django.db import models
from django.conf import settings
from directory.models import DISTRICT_CHOICES, STATE_CHOICES, ApprovalFields


JOB_TYPE_CHOICES = [
	("full-time", "Full Time"),
	("part-time", "Part Time"),
	("contract", "Contract"),
	("freelance", "Freelance"),
	("temporary", "Temporary"),
	("internship", "Internship"),
]

EXPERIENCE_LEVEL_CHOICES = [
	("entry-level", "Entry Level (0-1 year)"),
	("junior", "Junior (1-3 years)"),
	("mid-level", "Mid Level (3-5 years)"),
	("senior", "Senior (5-10 years)"),
	("expert", "Expert (10+ years)"),
]

EDUCATION_LEVEL_CHOICES = [
	("high-school", "High School"),
	("diploma", "Diploma"),
	("bachelor", "Bachelor's Degree"),
	("master", "Master's Degree"),
	("phd", "PhD"),
	("not-specified", "Not Specified"),
]


class JobCategory(models.Model):
	name = models.CharField(max_length=100, unique=True)
	description = models.TextField(blank=True)
	icon = models.CharField(max_length=50, blank=True)

	class Meta:
		verbose_name_plural = "Job Categories"
		ordering = ["name"]

	def __str__(self):
		return self.name


class Job(ApprovalFields):
	posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posted_jobs")
	title = models.CharField(max_length=200)
	description = models.TextField()
	category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True)
	job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
	experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES)
	education_level = models.CharField(max_length=30, choices=EDUCATION_LEVEL_CHOICES, default="not-specified")
	
	district = models.CharField(max_length=100, choices=DISTRICT_CHOICES)
	state = models.CharField(max_length=100, choices=STATE_CHOICES, default="Andhra Pradesh")
	city_area = models.CharField(max_length=100, blank=True)
	
	salary_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	salary_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	currency = models.CharField(max_length=3, default="INR")
	
	company_name = models.CharField(max_length=200)
	company_email = models.EmailField()
	company_phone = models.CharField(max_length=20)
	company_website = models.URLField(blank=True)
	
	skills_required = models.TextField(help_text="Comma-separated list of required skills")
	benefits = models.TextField(blank=True)
	application_link = models.URLField(blank=True)
	application_email = models.EmailField(blank=True)
	
	posted_date = models.DateTimeField(auto_now_add=True)
	deadline = models.DateTimeField(blank=True, null=True)

	class Meta:
		ordering = ["-posted_date"]

	def __str__(self):
		return f"{self.title} at {self.company_name}"


class JobApplication(models.Model):
	STATUS_CHOICES = [
		("applied", "Applied"),
		("under-review", "Under Review"),
		("shortlisted", "Shortlisted"),
		("rejected", "Rejected"),
	]

	job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
	applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="applied")
	
	resume_url = models.URLField(blank=True)
	cover_letter = models.TextField(blank=True)
	applied_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ("job", "applicant")
		ordering = ["-applied_at"]

	def __str__(self):
		return f"{self.applicant} - {self.job.title}"
