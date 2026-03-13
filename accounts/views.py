from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import View
from datetime import timedelta
from secrets import randbelow

from .forms import LoginForm, OTPRequestForm, OTPVerifyForm
from .models import OTPChallenge
from .otp_services import OTPDeliveryError, send_otp_code


class LoginView(View):
	template_name = "accounts/login.html"

	def get(self, request):
		if request.user.is_authenticated:
			return redirect("core:dashboard")
		form = LoginForm(request=request)
		return render(request, self.template_name, {"form": form})

	def post(self, request):
		form = LoginForm(request.POST, request=request)
		if form.is_valid():
			login(request, form.get_user())
			messages.success(request, "Welcome back to JBAC.")
			return redirect("core:dashboard")
		return render(request, self.template_name, {"form": form})


def logout_view(request):
	if request.user.is_authenticated:
		logout(request)
		messages.info(request, "You have been signed out.")
	return redirect("core:home")


class OTPRequestView(View):
	template_name = "accounts/otp_request.html"

	def _request_ip(self, request):
		forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
		if forwarded_for:
			return forwarded_for.split(",")[0].strip()
		return request.META.get("REMOTE_ADDR")

	def get(self, request):
		form = OTPRequestForm()
		return render(request, self.template_name, {"form": form})

	def post(self, request):
		form = OTPRequestForm(request.POST)
		if not form.is_valid():
			return render(request, self.template_name, {"form": form})

		user = form.get_user()
		identifier = form.cleaned_data["identifier"]
		now = timezone.now()
		window_start = now - timedelta(minutes=settings.OTP_REQUEST_WINDOW_MINUTES)

		recent_requests = OTPChallenge.objects.filter(
			identifier=identifier,
			role=user.role,
			created_at__gte=window_start,
		).count()
		if recent_requests >= settings.OTP_MAX_REQUESTS_PER_WINDOW:
			messages.error(
				request,
				"Too many OTP requests. Please wait before requesting another code.",
			)
			return render(request, self.template_name, {"form": form})

		code = f"{randbelow(1000000):06d}"
		challenge = OTPChallenge.objects.create(
			user=user,
			role=user.role,
			identifier=identifier,
			request_ip=self._request_ip(request),
			code=code,
			expires_at=now + timedelta(minutes=10),
		)
		request.session["otp_challenge_id"] = challenge.pk

		try:
			channel = send_otp_code(user, code)
		except OTPDeliveryError as exc:
			messages.error(request, str(exc))
			challenge.delete()
			request.session.pop("otp_challenge_id", None)
			return render(request, self.template_name, {"form": form})

		if channel == "sms":
			messages.success(request, "An OTP has been sent to your mobile number.")
		elif channel == "email":
			messages.success(request, "An OTP has been sent to your registered email.")
		else:
			messages.success(request, "OTP generated for your account.")

		if settings.DEBUG:
			messages.info(request, f"Development OTP: {code}")

		return redirect("accounts:otp-verify")


class OTPVerifyView(View):
	template_name = "accounts/otp_verify.html"

	def _get_challenge(self, request):
		challenge_id = request.session.get("otp_challenge_id")
		if not challenge_id:
			return None
		return OTPChallenge.objects.filter(pk=challenge_id).select_related("user").first()

	def get(self, request):
		challenge = self._get_challenge(request)
		if challenge is None:
			messages.error(request, "Start OTP login again.")
			return redirect("accounts:otp-request")
		form = OTPVerifyForm()
		return render(request, self.template_name, {"form": form, "challenge": challenge})

	def post(self, request):
		challenge = self._get_challenge(request)
		if challenge is None:
			messages.error(request, "Start OTP login again.")
			return redirect("accounts:otp-request")
		if challenge.is_locked():
			messages.error(request, "This OTP is temporarily locked due to multiple failed attempts.")
			return render(request, self.template_name, {"form": OTPVerifyForm(), "challenge": challenge})

		form = OTPVerifyForm(request.POST)
		if not form.is_valid():
			return render(request, self.template_name, {"form": form, "challenge": challenge})

		if not challenge.is_valid() or challenge.code != form.cleaned_data["code"]:
			challenge.failed_attempts += 1
			if challenge.failed_attempts >= settings.OTP_MAX_VERIFY_ATTEMPTS:
				challenge.locked_until = timezone.now() + timedelta(minutes=settings.OTP_LOCK_MINUTES)
			challenge.save(update_fields=["failed_attempts", "locked_until"])
			messages.error(request, "Invalid or expired OTP.")
			return render(request, self.template_name, {"form": form, "challenge": challenge})

		challenge.is_used = True
		challenge.save(update_fields=["is_used"])
		login(request, challenge.user, backend="django.contrib.auth.backends.ModelBackend")
		request.session.pop("otp_challenge_id", None)
		messages.success(request, "OTP login successful.")
		return redirect("core:dashboard")
