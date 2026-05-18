from django.contrib import admin

from .models import AboutPageContent, NavigationGroup, NavigationItem


@admin.register(AboutPageContent)
class AboutPageContentAdmin(admin.ModelAdmin):
	list_display = ("section_slug", "menu_title_en", "sort_order", "is_active", "updated_at")
	list_filter = ("is_active",)
	search_fields = ("section_slug", "menu_title_en", "menu_title_te", "page_title_en", "page_title_te", "youtube_embed_url")
	ordering = ("sort_order", "menu_title_en")
	fieldsets = (
		(
			"Section titles",
			{
				"fields": (
					"section_slug",
					"menu_title_te",
					"menu_title_en",
					"page_title_te",
					"page_title_en",
				),
			},
		),
		(
			"Content",
			{
				"fields": ("description", "points_text", "youtube_embed_url", "image", "pdf"),
			},
		),
		(
			"Visibility",
			{
				"fields": ("sort_order", "is_active"),
			},
		),
	)


class NavigationItemInline(admin.TabularInline):
	model = NavigationItem
	extra = 0
	fields = (
		"title_te",
		"title_en",
		"url_name",
		"url_path",
		"sort_order",
		"requires_auth",
		"staff_only",
		"open_in_new_tab",
		"is_active",
	)
	show_change_link = True


@admin.register(NavigationGroup)
class NavigationGroupAdmin(admin.ModelAdmin):
	list_display = ("slug", "title_en", "sort_order", "is_active", "updated_at")
	list_filter = ("is_active",)
	search_fields = ("slug", "title_en", "title_te", "prompt_title_en", "prompt_title_te")
	ordering = ("sort_order", "title_en")
	inlines = (NavigationItemInline,)
	fieldsets = (
		(
			"Titles",
			{
				"fields": (
					"slug",
					"title_te",
					"title_en",
					"prompt_title_te",
					"prompt_title_en",
				),
			},
		),
		(
			"Prompt text",
			{
				"fields": ("prompt_message_te", "prompt_message_en"),
			},
		),
		(
			"Visibility",
			{
				"fields": ("sort_order", "is_active"),
			},
		),
	)


@admin.register(NavigationItem)
class NavigationItemAdmin(admin.ModelAdmin):
	list_display = ("title_en", "group", "sort_order", "requires_auth", "staff_only", "is_active", "updated_at")
	list_filter = ("is_active", "requires_auth", "staff_only", "group")
	search_fields = ("title_en", "title_te", "url_name", "url_path", "group__title_en", "group__slug")
	ordering = ("group__sort_order", "sort_order", "title_en")
	fieldsets = (
		(
			"Menu item",
			{
				"fields": (
					"group",
					"title_te",
					"title_en",
					"url_name",
					"url_kwargs",
					"url_path",
				),
			},
		),
		(
			"Display rules",
			{
				"fields": ("sort_order", "requires_auth", "staff_only", "open_in_new_tab", "is_active"),
			},
		),
	)

