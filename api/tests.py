from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from directory.models import ChurchProfile, PastorProfile
from updates.models import NewsArticle


class APITests(TestCase):
	def setUp(self):
		self.pastor_user = User.objects.create_user(
			mobile_number="9000000002",
			email="pastor@example.com",
			password="Secret123!",
			role=User.Role.PASTOR,
		)
		PastorProfile.objects.create(
			user=self.pastor_user,
			pastor_name="Daniel",
			gender="male",
			church_name="Grace Church",
			church_address="Main Road",
			district="Guntur",
			state="Andhra Pradesh",
			years_of_ministry=8,
			is_approved=True,
			is_public=True,
		)

		self.church_user = User.objects.create_user(
			mobile_number="9000000003",
			email="church@example.com",
			password="Secret123!",
			role=User.Role.CHURCH,
		)
		ChurchProfile.objects.create(
			user=self.church_user,
			church_name="Hope Fellowship",
			pastor_name="Samuel",
			address="Center Street",
			village="Vijayawada",
			district="Krishna",
			state="Andhra Pradesh",
			latitude=16.5100,
			longitude=80.6400,
			is_approved=True,
			is_public=True,
		)

		NewsArticle.objects.create(
			title="Community Prayer Meet",
			summary="Monthly prayer update",
			content="Prayer meet on Sunday.",
			published_at=timezone.now(),
			is_published=True,
		)

	def test_stats_api(self):
		response = self.client.get(reverse("api:stats"))
		self.assertEqual(response.status_code, 200)
		payload = response.json()
		self.assertEqual(payload["status"], "ok")
		self.assertGreaterEqual(payload["data"]["pastors"], 1)

	def test_pastors_api_filter(self):
		response = self.client.get(reverse("api:pastors"), {"q": "Daniel"})
		self.assertEqual(response.status_code, 200)
		payload = response.json()
		self.assertEqual(payload["count"], 1)
		self.assertEqual(payload["data"][0]["church_name"], "Grace Church")

	def test_churches_api(self):
		response = self.client.get(reverse("api:churches"), {"district": "Krishna"})
		self.assertEqual(response.status_code, 200)
		payload = response.json()
		self.assertEqual(payload["count"], 1)
		self.assertEqual(payload["data"][0]["church_name"], "Hope Fellowship")

	def test_news_api(self):
		response = self.client.get(reverse("api:news"))
		self.assertEqual(response.status_code, 200)
		payload = response.json()
		self.assertEqual(payload["count"], 1)
		self.assertEqual(payload["data"][0]["title"], "Community Prayer Meet")