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
	services.prompt_title_te = "Hey user!"
	services.prompt_title_en = "Hey user!"
	services.prompt_message_te = "Hey user please login to get the more services"
	services.prompt_message_en = "Hey user please login to get the more services"
	services.sort_order = 1
	services.is_active = True
	services.save(update_fields=["title_te", "title_en", "prompt_title_te", "prompt_title_en", "prompt_message_te", "prompt_message_en", "sort_order", "is_active"])

	account.title_te = "Account"
	account.title_en = "Account"
	account.prompt_title_te = "Hey user!"
	account.prompt_title_en = "Hey user!"
	account.prompt_message_te = "Hey user please login to get the more services"
	account.prompt_message_en = "Hey user please login to get the more services"
	account.sort_order = 2
	account.is_active = True
	account.save(update_fields=["title_te", "title_en", "prompt_title_te", "prompt_title_en", "prompt_message_te", "prompt_message_en", "sort_order", "is_active"])

	service_items = [
		("Christian Organizations", "Christian Organizations", "directory:search", {}, "", 1),
		("Marriages", "Marriages", "meetings:view", {}, "", 2),
		("Jobs", "Jobs", "updates:list", {}, "", 3),
		("For Help", "For Help", "core:contact", {}, "", 4),
		("Search Business/House Rent Information", "Search Business/House Rent Information", "directory:search", {}, "", 5),
		("JBAC wings Information", "JBAC wings Information", "core:about-us", {}, "", 6),
		("Search Organization", "Search Organization", "directory:search", {}, "", 7),
	]

	account_items = [
		("Enter your church timings", "Enter your church timings", "meetings:submit", {}, "", 1),
		("Add wings under your ministry", "Add wings under your ministry", "updates:submit", {}, "", 2),
		("Submit business Information", "Submit business Information", "updates:submit", {}, "", 3),
		("Marraige Registration", "Marraige Registration", "meetings:submit", {}, "", 4),
		("Job requirements submission", "Job requirements submission", "updates:submit", {}, "", 5),
		("Adds information submission", "Adds information submission", "updates:submit", {}, "", 6),
		("To update your profile", "To update your profile", "core:dashboard", {}, "", 7),
		("If you have registered as a leader", "If you have registered as a leader", "core:dashboard", {}, "", 8),
		("Downloads", "Downloads", "songs:books", {}, "", 9),
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
		prompt_title_te="Hey user!",
		prompt_title_en="Hey user!",
		prompt_message_te="Hey user please login to get the more services",
		prompt_message_en="Hey user please login to get the more services",
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