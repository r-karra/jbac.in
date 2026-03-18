from django.contrib import admin

from .models import AboutPageContent


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
				"fields": ("description", "points_text", "youtube_embed_url"),
			},
		),
		(
			"Visibility",
			{
				"fields": ("sort_order", "is_active"),
			},
		),
	)

