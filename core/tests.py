from django.test import TestCase
from django.core.management import call_command
from django.urls import reverse

from accounts.models import User

from .models import AboutPageContent, NavigationGroup


class AboutSubpageTests(TestCase):
	def test_about_root_hides_content_until_submenu_click(self):
		response = self.client.get(reverse("core:about-us"))
		self.assertEqual(response.status_code, 200)
		# Check for Telugu text (template is in Telugu)
		self.assertContains(response, "ఎటువంటి సబ్‌మెను కంటెంట్ ఎంపిక కాలేదు")
		self.assertNotContains(response, "Secure registrations for believers")

	def test_about_subpage_uses_default_content_when_no_admin_rows(self):
		AboutPageContent.objects.all().delete()
		response = self.client.get(reverse("core:about-section", args=["about-us"]))
		self.assertEqual(response.status_code, 200)
		# Check for default section content - the description that should be present
		self.assertContains(response, "JBAC is a Christian community platform")

	def test_about_subpage_uses_admin_content_when_present(self):
		AboutPageContent.objects.update_or_create(
			section_slug="about-us",
			defaults={
				"menu_title_te": "మా గురించి",
				"menu_title_en": "About Us",
				"page_title_te": "మా గురించి అడ్మిన్",
				"page_title_en": "About Us Admin",
				"description": "Managed from admin.",
				"points_text": "Point 1\nPoint 2",
				"sort_order": 1,
				"is_active": True,
			},
		)
		response = self.client.get(reverse("core:about-section", args=["about-us"]))
		self.assertEqual(response.status_code, 200)
		# Check that the admin content is displayed
		self.assertContains(response, "మా గురించి అడ్మిన్")  # Telugu title
		self.assertContains(response, "Managed from admin.")


class AboutSeedCommandTests(TestCase):
	def test_seed_command_updates_existing_rows(self):
		AboutPageContent.objects.update_or_create(
			section_slug="about-us",
			defaults={
				"menu_title_te": "మా గురించి",
				"menu_title_en": "About Us",
				"page_title_te": "టెస్ట్",
				"page_title_en": "Temp Title",
				"description": "Temporary description.",
				"points_text": "Temp point",
				"sort_order": 1,
				"is_active": True,
			},
		)

		call_command("seed_about_pages")
		updated = AboutPageContent.objects.get(section_slug="about-us")
		self.assertEqual(updated.page_title_en, "About Us")
		self.assertIn("JBAC", updated.description)

	def test_seed_command_reset_removes_custom_rows(self):
		AboutPageContent.objects.create(
			section_slug="custom-temp",
			menu_title_te="కస్టమ్",
			menu_title_en="Custom",
			page_title_te="కస్టమ్ పేజీ",
			page_title_en="Custom Page",
			description="Custom page.",
			points_text="Custom point",
			sort_order=90,
			is_active=True,
		)

		call_command("seed_about_pages", reset=True)
		self.assertFalse(AboutPageContent.objects.filter(section_slug="custom-temp").exists())
		self.assertTrue(AboutPageContent.objects.filter(section_slug="about-us").exists())


class NavigationTests(TestCase):
	def setUp(self):
		self.client = self.client_class()
		self.group = NavigationGroup.objects.get(slug="services")
		self.user = User.objects.create_user(
			mobile_number="9000000010",
			email="member10@example.com",
			password="Secret123!",
			role=User.Role.BELIEVER,
		)

	def test_guest_navigation_group_shows_login_prompt(self):
		response = self.client.get(reverse("core:navigation-group", args=["services"]))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Hey user please login to get the more services")
		self.assertContains(response, "Login")

	def test_authenticated_navigation_group_shows_items(self):
		self.client.force_login(self.user)
		response = self.client.get(reverse("core:navigation-group", args=["services"]))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Christian Organizations")
		self.assertContains(response, "Marriages")
		self.assertContains(response, "Downloads")
		self.assertNotContains(response, "Hey user please login to get the more services")

	def test_home_page_exposes_services_and_account_labels(self):
		response = self.client.get(reverse("core:home"))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Services")
		self.assertContains(response, "Account")
