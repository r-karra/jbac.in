from django.contrib import admin

from .models import NewsArticle



@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
	list_display = ("title", "published_at", "is_published", "is_featured")
	list_filter = ("is_published", "is_featured", "published_at")
	prepopulated_fields = {"slug": ("title",)}
	search_fields = ("title", "summary", "content")
