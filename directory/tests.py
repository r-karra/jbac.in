from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from .models import BelieverProfile


class MemberIdPdfTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			mobile_number="9000000004",
			email="believer@example.com",
			password="Secret123!",
			role=User.Role.BELIEVER,
		)
		BelieverProfile.objects.create(
			user=self.user,
			full_name="Rajesh Kumar",
			gender="male",
			is_approved=True,
		)

	def test_member_id_pdf_requires_login(self):
		response = self.client.get(reverse("directory:member-id"))
		self.assertEqual(response.status_code, 302)

	def test_member_id_pdf_download(self):
		self.client.login(mobile_number=self.user.mobile_number, password="Secret123!")
		response = self.client.get(reverse("directory:member-id"))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response["Content-Type"], "application/pdf")
		self.assertIn("attachment; filename=\"jbac-member-id.pdf\"", response["Content-Disposition"])
		self.assertTrue(response.content.startswith(b"%PDF"))
