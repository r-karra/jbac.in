from urllib.parse import parse_qs, urlparse

from django.db import models
from django.urls import NoReverseMatch, reverse


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
	youtube_embed_url = models.URLField(
		blank=True,
		help_text="Paste a YouTube watch/share/embed URL (e.g. https://youtu.be/... or https://www.youtube.com/watch?v=...).",
	)
	image = models.ImageField(
		upload_to="core/about/",
		blank=True,
		null=True,
		help_text="Upload an image related to this section (Christians, ministry work, etc.)",
	)
	pdf = models.FileField(
		upload_to="core/about/",
		blank=True,
		null=True,
		help_text="Upload a PDF document related to this section.",
	)
	sort_order = models.PositiveSmallIntegerField(default=10)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["sort_order", "menu_title_en"]

	def points(self):
		return [line.strip() for line in self.points_text.splitlines() if line.strip()]

	def youtube_embed_src(self):
		url = (self.youtube_embed_url or "").strip()
		if not url:
			return ""

		try:
			parsed = urlparse(url)
		except ValueError:
			return ""

		hostname = (parsed.hostname or "").lower()
		path = parsed.path or ""
		video_id = ""

		if hostname in {"youtu.be"}:
			video_id = path.strip("/")
		elif hostname in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
			if path == "/watch":
				video_id = parse_qs(parsed.query).get("v", [""])[0]
			elif path.startswith("/embed/"):
				video_id = path.split("/embed/", 1)[1].split("/", 1)[0]
			elif path.startswith("/shorts/"):
				video_id = path.split("/shorts/", 1)[1].split("/", 1)[0]

		if len(video_id) != 11 or any(ch not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for ch in video_id):
			return ""

		return f"https://www.youtube.com/embed/{video_id}"

	def __str__(self):
		return f"{self.menu_title_en} ({self.section_slug})"


class NavigationGroup(models.Model):
	slug = models.SlugField(max_length=80, unique=True)
	title_te = models.CharField(max_length=200)
	title_en = models.CharField(max_length=200)
	prompt_title_te = models.CharField(max_length=200)
	prompt_title_en = models.CharField(max_length=200)
	prompt_message_te = models.TextField()
	prompt_message_en = models.TextField()
	sort_order = models.PositiveSmallIntegerField(default=10)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["sort_order", "title_en"]

	def display_title(self):
		return self.title_te or self.title_en

	def prompt_title(self):
		return self.prompt_title_te or self.prompt_title_en

	def prompt_message(self):
		return self.prompt_message_te or self.prompt_message_en

	def __str__(self):
		return f"{self.title_en} ({self.slug})"


class NavigationItem(models.Model):
	group = models.ForeignKey(NavigationGroup, on_delete=models.CASCADE, related_name="items")
	title_te = models.CharField(max_length=200)
	title_en = models.CharField(max_length=200)
	url_name = models.CharField(max_length=200, blank=True)
	url_kwargs = models.JSONField(default=dict, blank=True)
	url_path = models.CharField(max_length=255, blank=True)
	sort_order = models.PositiveSmallIntegerField(default=10)
	is_active = models.BooleanField(default=True)
	requires_auth = models.BooleanField(default=True)
	staff_only = models.BooleanField(default=False)
	open_in_new_tab = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["sort_order", "title_en"]

	def display_title(self):
		return self.title_te or self.title_en

	def href(self):
		if self.url_path:
			return self.url_path
		if not self.url_name:
			return "#"
		try:
			if self.url_kwargs:
				return reverse(self.url_name, kwargs=self.url_kwargs)
			return reverse(self.url_name)
		except NoReverseMatch:
			return "#"

	def __str__(self):
		return f"{self.title_en} -> {self.group.title_en}"
