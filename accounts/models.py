from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.crypto import get_random_string


class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, mobile_number, password, **extra_fields):
		if not mobile_number:
			raise ValueError("A mobile number is required")

		email = self.normalize_email(extra_fields.get("email"))
		extra_fields["email"] = email or None
		user = self.model(mobile_number=mobile_number, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, mobile_number, password=None, **extra_fields):
		extra_fields.setdefault("is_staff", False)
		extra_fields.setdefault("is_superuser", False)
		return self._create_user(mobile_number, password, **extra_fields)

	def create_superuser(self, mobile_number, password, **extra_fields):
		extra_fields.setdefault("is_staff", True)
		extra_fields.setdefault("is_superuser", True)
		extra_fields.setdefault("role", "admin")

		if extra_fields.get("is_staff") is not True:
			raise ValueError("Superuser must have is_staff=True.")
		if extra_fields.get("is_superuser") is not True:
			raise ValueError("Superuser must have is_superuser=True.")

		return self._create_user(mobile_number, password, **extra_fields)


class User(AbstractUser):
	class Role(models.TextChoices):
		BELIEVER = "believer", "Believer"
		PASTOR = "pastor", "Pastor"
		STUDENT = "student", "Student"
		PASTOR_ASSOCIATION = "pastor_association", "Pastor Association"
		MINISTRY = "ministry", "Ministries"
		CHURCH = "church", "Church"
		ORGANIZATION = "organization", "Christian Organization / Company"
		ADMIN = "admin", "Admin"

	username = None
	member_id = models.CharField(max_length=24, unique=True, blank=True, null=True)
	email = models.EmailField(blank=True, null=True, unique=True)
	mobile_number = models.CharField(max_length=20, unique=True)
	role = models.CharField(max_length=32, choices=Role.choices)
	preferred_language = models.CharField(
		max_length=2,
		choices=(("en", "English"), ("te", "Telugu")),
		default="en",
	)
	confidentiality_acknowledged = models.BooleanField(default=False)

	USERNAME_FIELD = "mobile_number"
	REQUIRED_FIELDS = []

	objects = UserManager()

	def save(self, *args, **kwargs):
		if self.email == "":
			self.email = None
		if not self.member_id:
			role_prefix = (self.role or "user")[:3].upper()
			for _ in range(5):
				candidate = f"JBAC-{role_prefix}-{get_random_string(6, allowed_chars='0123456789')}"
				if not User.objects.filter(member_id=candidate).exists():
					self.member_id = candidate
					break
		super().save(*args, **kwargs)

	@property
	def display_name(self):
		full_name = self.get_full_name().strip()
		return full_name or self.mobile_number

	def __str__(self):
		return f"{self.display_name} ({self.get_role_display()})"


class OTPChallenge(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otp_challenges")
	role = models.CharField(max_length=32, choices=User.Role.choices)
	identifier = models.CharField(max_length=120)
	request_ip = models.GenericIPAddressField(blank=True, null=True)
	code = models.CharField(max_length=6)
	expires_at = models.DateTimeField()
	failed_attempts = models.PositiveSmallIntegerField(default=0)
	locked_until = models.DateTimeField(blank=True, null=True)
	is_used = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]

	def is_valid(self):
		now = timezone.now()
		is_locked = self.locked_until is not None and now < self.locked_until
		return (not self.is_used) and (not is_locked) and now <= self.expires_at

	def is_locked(self):
		return self.locked_until is not None and timezone.now() < self.locked_until

	def __str__(self):
		return f"OTP for {self.user.mobile_number} ({self.role})"
