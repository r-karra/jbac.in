from django.db import migrations


def update_navigation(apps, schema_editor):
	NavigationGroup = apps.get_model("core", "NavigationGroup")
	NavigationItem = apps.get_model("core", "NavigationItem")

	services = NavigationGroup.objects.get(slug="services")
	account = NavigationGroup.objects.get(slug="account")

	NavigationItem.objects.filter(group=services).delete()
	NavigationItem.objects.filter(group=account).delete()

	# Update group metadata
	services.title_te = "సేవలు"
	services.title_en = "Services"
	services.prompt_title_te = "నమోదు చేయండి"
	services.prompt_title_en = "Please Register"
	services.prompt_message_te = "సేవలను ఉపయోగించుటకు దయచేసి లాగిన్ చేయండి"
	services.prompt_message_en = "Dear user, please login to use more services."
	services.sort_order = 1
	services.is_active = True
	services.save(update_fields=["title_te", "title_en", "prompt_title_te", "prompt_title_en", "prompt_message_te", "prompt_message_en", "sort_order", "is_active"])

	account.title_te = "ఖాతా"
	account.title_en = "Account"
	account.prompt_title_te = "నమోదు చేయండి"
	account.prompt_title_en = "Please Register"
	account.prompt_message_te = "ఖాతా సేవలను ఉపయోగించుటకు దయచేసి లాగిన్ చేయండి"
	account.prompt_message_en = "Dear user, please login to use account services."
	account.sort_order = 2
	account.is_active = True
	account.save(update_fields=["title_te", "title_en", "prompt_title_te", "prompt_title_en", "prompt_message_te", "prompt_message_en", "sort_order", "is_active"])

	# ========================================================================
	# SERVICES MENU ITEMS (8 Search/Browse Pages matching reference)
	# ========================================================================
	service_items = [
		("ఉదాహరణ", "Institutes", "core:institutes-search", {}, "", 1),
		("వివాహాలు", "Marriages", "core:marriages-search", {}, "", 2),
		("ఉద్యోగాలు", "Jobs", "core:jobs-search", {}, "", 3),
		("సహాయం కోసం శోధన", "Search For Help", "core:help-search", {}, "", 4),
		("విశ్వాస సংబంధిత సమాచారం", "Update News", "updates:list", {}, "", 5),
		("వ్యాపారం", "Business", "core:business-search", {}, "", 6),
		("JBAC శాఖలు", "Wings", "core:wings-search", {}, "", 7),
		("సంస్థలు", "Organization", "core:organization-search", {}, "", 8),
	]

	# ========================================================================
	# ACCOUNT MENU ITEMS (11 Forms matching reference)
	# ========================================================================
	account_items = [
		("చర్చి సమయాలు", "Church Timings", "core:church-timings-submit", {}, "", 1),
		("సమావేశ సమర్పణ", "Meetings Information", "core:meetings-submit", {}, "", 2),
		("ఉదాహరణ సమర్పణ", "Institute", "core:institute-submit", {}, "", 3),
		("వ్యాపారం సమర్పణ", "Business", "core:business-submit", {}, "", 4),
		("వివాహ నమోదు", "Marriages", "core:marriages-submit", {}, "", 5),
		("ఘటనల నివేదన", "Attacks", "core:attacks-submit", {}, "", 6),
		("ఉద్యోగ సమర్పణ", "Jobs", "core:jobs-submit", {}, "", 7),
		("ప్రకటనలు", "Ads", "core:ads-submit", {}, "", 8),
		("ప్రొఫైల్‌ను సవరించండి", "Edit Profile", "core:dashboard", {}, "", 9),
		("నాయకుల నమోదు", "Leaders", "core:leaders-submit", {}, "", 10),
		("డౌన్‌లోడ్‌లు", "Downloads", "core:downloads", {}, "", 11),
	]

	# Create service items (8 search pages)
	for title_te, title_en, url_name, url_kwargs, url_path, sort_order in service_items:
		NavigationItem.objects.create(
			group=services,
			title_te=title_te,
			title_en=title_en,
			url_name=url_name,
			url_kwargs=url_kwargs,
			url_path=url_path,
			sort_order=sort_order,
			is_active=True,
			requires_auth=False,  # Search/browse pages should be public
			staff_only=False,
			open_in_new_tab=False,
		)

	# Create account items (11 submission forms)
	for title_te, title_en, url_name, url_kwargs, url_path, sort_order in account_items:
		NavigationItem.objects.create(
			group=account,
			title_te=title_te,
			title_en=title_en,
			url_name=url_name,
			url_kwargs=url_kwargs,
			url_path=url_path,
			sort_order=sort_order,
			is_active=True,
			requires_auth=True,  # All account functions require login
			staff_only=False,
			open_in_new_tab=False,
		)


def reverse_navigation(apps, schema_editor):
	NavigationGroup = apps.get_model("core", "NavigationGroup")
	NavigationItem = apps.get_model("core", "NavigationItem")
	NavigationItem.objects.filter(group__slug__in=["services", "account"]).delete()


class Migration(migrations.Migration):

	dependencies = [
		("core", "0007_gallerycategory_galleryimage_prayer"),
	]

	operations = [
		migrations.RunPython(update_navigation, reverse_navigation),
	]
