from django.db import models
from django.utils.text import slugify



class NewsArticle(models.Model):
	title = models.CharField(max_length=300)
	slug = models.SlugField(max_length=320, unique=True, blank=True)
	summary = models.TextField(blank=True)
	content = models.TextField()
	published_at = models.DateTimeField()
	is_published = models.BooleanField(default=True)
	is_featured = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-published_at", "-created_at"]

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		super().save(*args, **kwargs)

	def __str__(self):
		return self.title
