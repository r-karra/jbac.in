from django.db import models
from django.conf import settings


DISTRICT_CHOICES = [
	("Alluri Sitharama Raju", "Alluri Sitharama Raju"),
	("Anakapalli", "Anakapalli"),
	("Anantapuramu", "Anantapuramu"),
	("Annamayya", "Annamayya"),
	("Bapatla", "Bapatla"),
	("Chittoor", "Chittoor"),
	("Dr. B.R. Ambedkar Konaseema", "Dr. B.R. Ambedkar Konaseema"),
	("East Godavari", "East Godavari"),
	("Eluru", "Eluru"),
	("Guntur", "Guntur"),
	("Kakinada", "Kakinada"),
	("Krishna", "Krishna"),
	("Kurnool", "Kurnool"),
	("Nandyal", "Nandyal"),
	("Nellore", "Nellore"),
	("NTR", "NTR"),
	("Palnadu", "Palnadu"),
	("Parvathipuram Manyam", "Parvathipuram Manyam"),
	("Prakasam", "Prakasam"),
	("Srikakulam", "Srikakulam"),
	("Sri Potti Sriramulu Nellore", "Sri Potti Sriramulu Nellore"),
	("Sri Sathya Sai", "Sri Sathya Sai"),
	("Tirupati", "Tirupati"),
	("Visakhapatnam", "Visakhapatnam"),
	("Vizianagaram", "Vizianagaram"),
	("West Godavari", "West Godavari"),
	("YSR Kadapa", "YSR Kadapa"),
]

STATE_CHOICES = [
	("Andhra Pradesh", "Andhra Pradesh"),
	("Telangana", "Telangana"),
	("Other", "Other"),
]


class ApprovalFields(models.Model):
	is_approved = models.BooleanField(default=False)
	is_public = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class BelieverProfile(ApprovalFields):
	class Gender(models.TextChoices):
		MALE = "male", "Male"
		FEMALE = "female", "Female"
		OTHER = "other", "Other"

	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="believer_profile")
	full_name = models.CharField(max_length=200)
	gender = models.CharField(max_length=20, choices=Gender.choices)
	whatsapp_number = models.CharField(max_length=20, blank=True)
	date_of_birth = models.DateField(blank=True, null=True)
	life_goal = models.TextField(blank=True)
	hobbies = models.TextField(blank=True)
	youtube_channel = models.URLField(blank=True)
	additional_information = models.TextField(blank=True)

	def __str__(self):
		return self.full_name


class PastorProfile(ApprovalFields):
	class Gender(models.TextChoices):
		MALE = "male", "Male"
		FEMALE = "female", "Female"
		OTHER = "other", "Other"

	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pastor_profile")
	pastor_name = models.CharField(max_length=200)
	gender = models.CharField(max_length=20, choices=Gender.choices)
	church_name = models.CharField(max_length=200)
	church_address = models.TextField()
	district = models.CharField(max_length=100, choices=DISTRICT_CHOICES)
	state = models.CharField(max_length=100, choices=STATE_CHOICES, default="Andhra Pradesh")
	latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
	longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
	years_of_ministry = models.PositiveIntegerField(default=0)
	additional_information = models.TextField(blank=True)

	class Meta:
		ordering = ["pastor_name"]

	def __str__(self):
		return f"{self.pastor_name} - {self.church_name}"


class StudentProfile(ApprovalFields):
	class Gender(models.TextChoices):
		MALE = "male", "Male"
		FEMALE = "female", "Female"
		OTHER = "other", "Other"

	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile")
	student_name = models.CharField(max_length=200)
	gender = models.CharField(max_length=20, choices=Gender.choices)
	college_name = models.CharField(max_length=200)
	course = models.CharField(max_length=200)
	year_of_study = models.CharField(max_length=100)
	district = models.CharField(max_length=100, choices=DISTRICT_CHOICES)
	state = models.CharField(max_length=100, choices=STATE_CHOICES, default="Andhra Pradesh")

	def __str__(self):
		return self.student_name


class ChurchProfile(ApprovalFields):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="church_profile")
	church_name = models.CharField(max_length=200)
	pastor_name = models.CharField(max_length=200)
	address = models.TextField()
	village = models.CharField(max_length=200, blank=True)
	district = models.CharField(max_length=100, choices=DISTRICT_CHOICES)
	state = models.CharField(max_length=100, choices=STATE_CHOICES, default="Andhra Pradesh")
	latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
	longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
	year_established = models.PositiveIntegerField(blank=True, null=True)
	ministry_details = models.TextField(blank=True)

	class Meta:
		ordering = ["church_name"]

	def __str__(self):
		return self.church_name


class OrganizationProfile(ApprovalFields):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="organization_profile")
	organization_name = models.CharField(max_length=200)
	founder_name = models.CharField(max_length=200)
	address = models.TextField()
	district = models.CharField(max_length=100, choices=DISTRICT_CHOICES)
	state = models.CharField(max_length=100, choices=STATE_CHOICES, default="Andhra Pradesh")
	website = models.URLField(blank=True)
	ministry_type = models.CharField(max_length=200, blank=True)

	class Meta:
		ordering = ["organization_name"]

	def __str__(self):
		return self.organization_name


def get_profile_for_user(user):
	if not user.is_authenticated:
		return None

	profile_lookup = {
		user.Role.BELIEVER: "believer_profile",
		user.Role.PASTOR: "pastor_profile",
		user.Role.STUDENT: "student_profile",
		user.Role.CHURCH: "church_profile",
		user.Role.PASTOR_ASSOCIATION: "organization_profile",
		user.Role.MINISTRY: "organization_profile",
		user.Role.ORGANIZATION: "organization_profile",
	}
	relation = profile_lookup.get(user.role)
	return getattr(user, relation, None) if relation else None
