from django.db import models
from django.utils.text import slugify


NEWSPAPER_CHOICES = [
	("andhra-jyothi", "Andhra Jyothi"),
	("eenadu", "Eenadu"),
	("sakshi", "Sakshi"),
	("deccan-chronicle", "Deccan Chronicle"),
	("the-hindu", "The Hindu"),
	("times-of-india", "Times of India"),
	("indian-express", "Indian Express"),
	("other", "Other"),
]

NEWS_CATEGORY_CHOICES = [
	("christian-media", "News related to Christian media"),
	("honorarium", "News related to Honorarium, Government schemes"),
	("christians", "News related to Christians"),
	("general", "General News"),
	("medical-council", "News related to Delhi Christian Medical Council"),
	("education", "Education related"),
	("training", "Training related"),
	("jobs", "Jobs related"),
	("health", "Health related"),
	("society", "News related to problems in society"),
	("dr-joseph", "News about Dr. Joseph Prakash Mosiganti"),
]


class NewsArticle(models.Model):
	title = models.CharField(max_length=300)
	slug = models.SlugField(max_length=320, unique=True, blank=True)
	image = models.ImageField(upload_to="updates/news/", blank=True, null=True)
	image_url = models.URLField(blank=True)
	youtube_embed_url = models.URLField(blank=True)
	summary = models.TextField(blank=True)
	content = models.TextField()
	newspaper = models.CharField(
		max_length=50,
		choices=NEWSPAPER_CHOICES,
		blank=True,
		help_text="Select the newspaper this news is from",
	)
	category = models.CharField(
		max_length=50,
		choices=NEWS_CATEGORY_CHOICES,
		default="general",
		help_text="Select the news category",
	)
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

	@property
	def display_image_url(self):
		if self.image:
			return self.image.url
		return self.image_url
