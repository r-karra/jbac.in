from urllib.parse import parse_qs, urlparse

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
	youtube_embed_url = models.URLField(
		blank=True,
		help_text="Paste a YouTube watch/share/embed URL (e.g. https://youtu.be/... or https://www.youtube.com/watch?v=...).",
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
