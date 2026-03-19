from django.contrib import admin

from .models import NewsArticle



@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
	list_display = (
		"title",
		"published_at",
		"is_published",
		"is_featured",
		"has_image",
		"has_youtube_embed",
	)
	list_filter = ("is_published", "is_featured", "published_at")
	prepopulated_fields = {"slug": ("title",)}
	search_fields = ("title", "summary", "content", "image_url", "youtube_embed_url")
	fields = (
		"title",
		"slug",
		"image",
		"image_url",
		"youtube_embed_url",
		"summary",
		"content",
		"published_at",
		"is_published",
		"is_featured",
	)

	@admin.display(boolean=True, description="Image")
	def has_image(self, obj):
		return bool(obj.image or obj.image_url)

	@admin.display(boolean=True, description="YouTube")
	def has_youtube_embed(self, obj):
		return bool(obj.youtube_embed_url)
