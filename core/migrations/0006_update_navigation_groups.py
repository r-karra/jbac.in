from django.db import migrations


def update_navigation(apps, schema_editor):
	NavigationGroup = apps.get_model("core", "NavigationGroup")
	NavigationItem = apps.get_model("core", "NavigationItem")

	services = NavigationGroup.objects.get(slug="services")
	account = NavigationGroup.objects.get(slug="account")

	NavigationItem.objects.filter(group=services).delete()
	NavigationItem.objects.filter(group=account).delete()

	services.title_te = "Services"
	services.title_en = "Services"
	services.prompt_title_te = "Login Required"
	services.prompt_title_en = "Login Required"
	services.prompt_message_te = "Dear user, please login to use more services."
	services.prompt_message_en = "Dear user, please login to use more services."
	services.sort_order = 1
	services.is_active = True
	services.save(update_fields=["title_te", "title_en", "prompt_title_te", "prompt_title_en", "prompt_message_te", "prompt_message_en", "sort_order", "is_active"])

	account.title_te = "Account"
	account.title_en = "Account"
	account.prompt_title_te = "Login Required"
	account.prompt_title_en = "Login Required"
	account.prompt_message_te = "Dear user, please login to use more services."
	account.prompt_message_en = "Dear user, please login to use more services."
	account.sort_order = 2
	account.is_active = True
	account.save(update_fields=["title_te", "title_en", "prompt_title_te", "prompt_title_en", "prompt_message_te", "prompt_message_en", "sort_order", "is_active"])

	service_items = [
		("Jobs", "Jobs", "core:job-submission", {}, "", 1),
		("Businesses", "Businesses", "core:business-submission", {}, "", 2),
		("Institutes", "Educational Institutes", "core:institute-submission", {}, "", 3),
		("Prayer Requests", "Prayer Requests", "core:prayer-submission", {}, "", 4),
		("Incident Reporting", "Report an Incident", "core:incident-report", {}, "", 5),
	]

	account_items = [
		("My Dashboard", "My Dashboard", "core:dashboard", {}, "", 1),
		("My Submissions", "View My Submissions", "core:dashboard", {}, "", 2),
		("Edit Profile", "Edit Profile", "core:dashboard", {}, "", 3),
	]

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
			requires_auth=True,
			staff_only=False,
			open_in_new_tab=False,
		)

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
			requires_auth=True,
			staff_only=False,
			open_in_new_tab=False,
		)


def reverse_navigation(apps, schema_editor):
	NavigationGroup = apps.get_model("core", "NavigationGroup")
	NavigationItem = apps.get_model("core", "NavigationItem")
	NavigationItem.objects.filter(group__slug__in=["services", "account"]).delete()
	NavigationGroup.objects.filter(slug__in=["services", "account"]).update(
		title_te="Services",
		title_en="Services",
		prompt_title_te="Login Required",
		prompt_title_en="Login Required",
		prompt_message_te="Dear user, please login to use more services.",
		prompt_message_en="Dear user, please login to use more services.",
	)
	NavigationGroup.objects.filter(slug="account").update(
		title_te="Account",
		title_en="Account",
	)


class Migration(migrations.Migration):

	dependencies = [
		("core", "0005_navigationgroup_navigationitem"),
	]

	operations = [
		migrations.RunPython(update_navigation, reverse_navigation),
	]