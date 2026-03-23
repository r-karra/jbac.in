from django import forms
from .models import NewsArticle, NEWSPAPER_CHOICES, NEWS_CATEGORY_CHOICES


class NewsSubmissionForm(forms.ModelForm):
	class Meta:
		model = NewsArticle
		fields = [
			"title",
			"image",
			"newspaper",
			"category",
			"summary",
			"content",
		]
		widgets = {
			"title": forms.TextInput(
				attrs={
					"class": "form-input",
					"placeholder": "సమాచారం శీర్షిక",
				}
			),
			"image": forms.ClearableFileInput(
				attrs={
					"class": "form-input",
					"accept": "image/*",
				}
			),
			"newspaper": forms.Select(
				attrs={"class": "form-select"}
			),
			"category": forms.Select(
				attrs={"class": "form-select"}
			),
			"summary": forms.Textarea(
				attrs={
					"class": "form-textarea",
					"placeholder": "సమాచారం సంక్షిప్త వివరణ",
					"rows": 3,
				}
			),
			"content": forms.Textarea(
				attrs={
					"class": "form-textarea",
					"placeholder": "సమాచారం పూర్తి విషయ సामగ్రి",
					"rows": 6,
				}
			),
		}
		labels = {
			"title": "సమాచారం శీర్షిక *",
			"image": "సమాచారానికి సంబందించిన ఫోటో అప్లోడ్",
			"newspaper": "సమాచారం గురించి వివరణ (ఏ పేపర్) *",
			"category": "సమాచారం ఏ కేటగిరీ క్రింద వస్తుంది *",
			"summary": "సమాచారం సంక్షిప్త సారాంశం",
			"content": "సమాచారం పూర్తి విషయ సామగ్రి *",
		}
		help_texts = {
			"image": "ఐచ్ఛికం - ఈ సమాచారానికి సంబందించిన ఫోటోను అప్లోడ్ చేయండి",
			"newspaper": "సమాచారం ఎందుకు/ఏ న్యూస్‌పేపర్ నుండి చేదా స్థానం నుండి వచ్చింది?",
			"category": "సమాచారం ఏ నిర్దిష్ట వర్గానికి చెందినది?",
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Set newspaper to optional (blank=True)
		self.fields["newspaper"].required = False
		self.fields["newspaper"].choices = [("", "--- ఎంచుకోండి (ఐచ్ఛికం) ---")] + list(NEWSPAPER_CHOICES)
		# Ensure category is required
		self.fields["category"].required = True
		self.fields["category"].choices = list(NEWS_CATEGORY_CHOICES)


class NewsAdminForm(forms.ModelForm):
	"""Extended form for admin with additional fields like image_url and youtube_embed_url"""
	class Meta:
		model = NewsArticle
		fields = [
			"title",
			"image",
			"image_url",
			"youtube_embed_url",
			"newspaper",
			"category",
			"summary",
			"content",
			"published_at",
			"is_published",
			"is_featured",
		]
		widgets = {
			"title": forms.TextInput(attrs={"class": "form-input"}),
			"image": forms.ClearableFileInput(attrs={"class": "form-input"}),
			"image_url": forms.URLInput(attrs={"class": "form-input"}),
			"youtube_embed_url": forms.URLInput(attrs={"class": "form-input"}),
			"newspaper": forms.Select(attrs={"class": "form-select"}),
			"category": forms.Select(attrs={"class": "form-select"}),
			"summary": forms.Textarea(attrs={"class": "form-textarea", "rows": 3}),
			"content": forms.Textarea(attrs={"class": "form-textarea", "rows": 6}),
			"published_at": forms.DateTimeInput(attrs={"class": "form-input", "type": "datetime-local"}),
		}
