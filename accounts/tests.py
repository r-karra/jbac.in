from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from .models import OTPChallenge, User


class OTPFlowTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			mobile_number="9000000001",
			email="member1@example.com",
			password="Secret123!",
			role=User.Role.BELIEVER,
		)

	@patch("accounts.views.send_otp_code", return_value="email")
	def test_otp_request_creates_challenge(self, _mock_send):
		response = self.client.post(
			reverse("accounts:otp-request"),
			{"role": User.Role.BELIEVER, "identifier": self.user.mobile_number},
		)
		self.assertRedirects(response, reverse("accounts:otp-verify"))
		challenge = OTPChallenge.objects.get(user=self.user)
		self.assertFalse(challenge.is_used)
		self.assertIn("otp_challenge_id", self.client.session)

	@patch("accounts.views.send_otp_code", return_value="console")
	def test_otp_verify_logs_user_in(self, _mock_send):
		self.client.post(
			reverse("accounts:otp-request"),
			{"role": User.Role.BELIEVER, "identifier": self.user.mobile_number},
		)
		challenge = OTPChallenge.objects.get(user=self.user)

		response = self.client.post(reverse("accounts:otp-verify"), {"code": challenge.code})
		self.assertRedirects(response, reverse("core:dashboard"))
		challenge.refresh_from_db()
		self.assertTrue(challenge.is_used)
		self.assertIn("_auth_user_id", self.client.session)

	@patch("accounts.views.send_otp_code", return_value="console")
	def test_otp_verify_rejects_invalid_code(self, _mock_send):
		self.client.post(
			reverse("accounts:otp-request"),
			{"role": User.Role.BELIEVER, "identifier": self.user.mobile_number},
		)
		response = self.client.post(reverse("accounts:otp-verify"), {"code": "000000"})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Invalid or expired OTP")

	@patch("accounts.views.send_otp_code", return_value="console")
	def test_otp_gets_locked_after_retries(self, _mock_send):
		self.client.post(
			reverse("accounts:otp-request"),
			{"role": User.Role.BELIEVER, "identifier": self.user.mobile_number},
		)
		for _ in range(5):
			self.client.post(reverse("accounts:otp-verify"), {"code": "111111"})

		challenge = OTPChallenge.objects.get(user=self.user)
		self.assertIsNotNone(challenge.locked_until)
		self.assertEqual(challenge.failed_attempts, 5)

	@patch("accounts.views.send_otp_code", return_value="console")
	def test_otp_request_rate_limit(self, _mock_send):
		for _ in range(5):
			self.client.post(
				reverse("accounts:otp-request"),
				{"role": User.Role.BELIEVER, "identifier": self.user.mobile_number},
			)
		response = self.client.post(
			reverse("accounts:otp-request"),
			{"role": User.Role.BELIEVER, "identifier": self.user.mobile_number},
		)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Too many OTP requests")
