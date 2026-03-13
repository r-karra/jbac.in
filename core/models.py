from django.db import models


class AboutPageContent(models.Model):
	section_slug = models.SlugField(max_length=80, unique=True)
	menu_title_te = models.CharField(max_length=200)
	menu_title_en = models.CharField(max_length=200)
	page_title_te = models.CharField(max_length=200)
	page_title_en = models.CharField(max_length=200)
	description = models.TextField()
	points_text = models.TextField(
		help_text="Use one line per bullet point.",
		blank=True,
	)
	sort_order = models.PositiveSmallIntegerField(default=10)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["sort_order", "menu_title_en"]

	def points(self):
		return [line.strip() for line in self.points_text.splitlines() if line.strip()]

	def __str__(self):
		return f"{self.menu_title_en} ({self.section_slug})"
