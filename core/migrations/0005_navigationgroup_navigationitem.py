from django.db import migrations, models


def seed_navigation(apps, schema_editor):
	NavigationGroup = apps.get_model("core", "NavigationGroup")
	NavigationItem = apps.get_model("core", "NavigationItem")

	services, _ = NavigationGroup.objects.update_or_create(
		slug="services",
		defaults={
			"title_te": "సేవలు",
			"title_en": "Services",
			"prompt_title_te": "హే యూజర్!",
			"prompt_title_en": "Hey user!",
			"prompt_message_te": "ఈ సేవలను ఉపయోగించడానికి దయచేసి లాగిన్ అవండి.",
			"prompt_message_en": "Please login to use these services.",
			"sort_order": 1,
			"is_active": True,
		},
	)

	account, _ = NavigationGroup.objects.update_or_create(
		slug="account",
		defaults={
			"title_te": "ఖాతా",
			"title_en": "Account",
			"prompt_title_te": "హే యూజర్!",
			"prompt_title_en": "Hey user!",
			"prompt_message_te": "ఈ సేవలను ఉపయోగించడానికి దయచేసి లాగిన్ అవండి.",
			"prompt_message_en": "Please login to use these services.",
			"sort_order": 2,
			"is_active": True,
		},
	)

	service_items = [
		{
			"title_te": "హోమ్",
			"title_en": "Home",
			"url_name": "core:home",
			"sort_order": 1,
		},
		{
			"title_te": "మా గురించి",
			"title_en": "About Us",
			"url_name": "core:about-us",
			"sort_order": 2,
		},
		{
			"title_te": "నమోదు కేంద్రం",
			"title_en": "Registration Center",
			"url_name": "directory:register",
			"sort_order": 3,
		},
		{
			"title_te": "శోధన",
			"title_en": "Search",
			"url_name": "directory:search",
			"sort_order": 4,
		},
		{
			"title_te": "జిల్లా మ్యాప్",
			"title_en": "District Map",
			"url_name": "directory:map-search",
			"sort_order": 5,
		},
		{
			"title_te": "సమావేశాలు",
			"title_en": "Meetings",
			"url_name": "meetings:view",
			"sort_order": 6,
		},
		{
			"title_te": "పాటలు & పుస్తకాలు",
			"title_en": "Songs & Books",
			"url_name": "songs:search",
			"sort_order": 7,
		},
		{
			"title_te": "వార్తలు",
			"title_en": "News",
			"url_name": "updates:list",
			"sort_order": 8,
		},
		{
			"title_te": "సంప్రదించండి",
			"title_en": "Contact",
			"url_name": "core:contact",
			"sort_order": 9,
		},
	]

	account_items = [
		{
			"title_te": "డాష్‌బోర్డ్",
			"title_en": "Dashboard",
			"url_name": "core:dashboard",
			"sort_order": 1,
		},
		{
			"title_te": "లాగ్ అవుట్",
			"title_en": "Logout",
			"url_name": "accounts:logout",
			"sort_order": 2,
		},
		{
			"title_te": "నిర్వాహక డాష్‌బోర్డ్",
			"title_en": "Admin Dashboard",
			"url_name": "core:admin-dashboard",
			"sort_order": 3,
			"staff_only": True,
		},
	]

	for item_data in service_items:
		NavigationItem.objects.update_or_create(
			group=services,
			title_en=item_data["title_en"],
			defaults={
				"title_te": item_data["title_te"],
				"url_name": item_data["url_name"],
				"url_kwargs": {},
				"url_path": "",
				"sort_order": item_data["sort_order"],
				"is_active": True,
				"requires_auth": True,
				"staff_only": False,
				"open_in_new_tab": False,
			},
		)

	for item_data in account_items:
		NavigationItem.objects.update_or_create(
			group=account,
			title_en=item_data["title_en"],
			defaults={
				"title_te": item_data["title_te"],
				"url_name": item_data["url_name"],
				"url_kwargs": {},
				"url_path": "",
				"sort_order": item_data["sort_order"],
				"is_active": True,
				"requires_auth": True,
				"staff_only": item_data.get("staff_only", False),
				"open_in_new_tab": False,
			},
		)


def unseed_navigation(apps, schema_editor):
	NavigationItem = apps.get_model("core", "NavigationItem")
	NavigationGroup = apps.get_model("core", "NavigationGroup")
	NavigationItem.objects.all().delete()
	NavigationGroup.objects.all().delete()


class Migration(migrations.Migration):

	dependencies = [
		("core", "0004_aboutpagecontent_image_aboutpagecontent_pdf"),
	]

	operations = [
		migrations.CreateModel(
			name="NavigationGroup",
			fields=[
				("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
				("slug", models.SlugField(max_length=80, unique=True)),
				("title_te", models.CharField(max_length=200)),
				("title_en", models.CharField(max_length=200)),
				("prompt_title_te", models.CharField(max_length=200)),
				("prompt_title_en", models.CharField(max_length=200)),
				("prompt_message_te", models.TextField()),
				("prompt_message_en", models.TextField()),
				("sort_order", models.PositiveSmallIntegerField(default=10)),
				("is_active", models.BooleanField(default=True)),
				("created_at", models.DateTimeField(auto_now_add=True)),
				("updated_at", models.DateTimeField(auto_now=True)),
			],
			options={
				"ordering": ["sort_order", "title_en"],
			},
		),
		migrations.CreateModel(
			name="NavigationItem",
			fields=[
				("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
				("title_te", models.CharField(max_length=200)),
				("title_en", models.CharField(max_length=200)),
				("url_name", models.CharField(blank=True, max_length=200)),
				("url_kwargs", models.JSONField(blank=True, default=dict)),
				("url_path", models.CharField(blank=True, max_length=255)),
				("sort_order", models.PositiveSmallIntegerField(default=10)),
				("is_active", models.BooleanField(default=True)),
				("requires_auth", models.BooleanField(default=True)),
				("staff_only", models.BooleanField(default=False)),
				("open_in_new_tab", models.BooleanField(default=False)),
				("created_at", models.DateTimeField(auto_now_add=True)),
				("updated_at", models.DateTimeField(auto_now=True)),
				(
					"group",
					models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="items", to="core.navigationgroup"),
				),
			],
			options={
				"ordering": ["sort_order", "title_en"],
			},
		),
		migrations.RunPython(seed_navigation, unseed_navigation),
	]