from django import forms
from django.core.exceptions import ValidationError

from .models import DENOMINATION_CHOICES, DISTRICT_CHOICES, MEETING_TYPE_CHOICES, MINISTRY_CHOICES, Meeting


class MeetingSubmissionForm(forms.ModelForm):
	class Meta:
		model = Meeting
		fields = [
			"title",
			"description",
			"start_date",
			"end_date",
			"organizer_name",
			"estimated_attendance",
			"organizer_phone",
			"address",
			"district",
			"state",
			"city_area",
			"mandal",
			"village",
			"meeting_type",
			"denomination",
			"ministry",
			"google_map_location",
			"latitude",
			"longitude",
			"poster",
			"youtube_link",
			"additional_info",
		]
		widgets = {
			"title": forms.TextInput(attrs={"class": "form-input", "placeholder": "Meeting Title / Meeting Name"}),
			"description": forms.Textarea(attrs={"class": "form-textarea", "placeholder": "Meeting Description"}),
			"start_date": forms.DateInput(attrs={"class": "form-input", "type": "date"}),
			"end_date": forms.DateInput(attrs={"class": "form-input", "type": "date"}),
			"organizer_name": forms.TextInput(attrs={"class": "form-input"}),
			"estimated_attendance": forms.NumberInput(attrs={"class": "form-input", "min": "1"}),
			"organizer_phone": forms.TextInput(attrs={"class": "form-input"}),
			"address": forms.Textarea(attrs={"class": "form-textarea", "rows": 3}),
			"district": forms.Select(attrs={"class": "form-select"}),
			"state": forms.TextInput(attrs={"class": "form-input", "placeholder": "Andhra Pradesh"}),
			"city_area": forms.TextInput(attrs={"class": "form-input"}),
			"mandal": forms.TextInput(attrs={"class": "form-input"}),
			"village": forms.TextInput(attrs={"class": "form-input"}),
			"meeting_type": forms.Select(attrs={"class": "form-select"}),
			"denomination": forms.Select(attrs={"class": "form-select"}),
			"ministry": forms.Select(attrs={"class": "form-select"}),
			"google_map_location": forms.URLInput(attrs={"class": "form-input", "placeholder": "https://maps.google.com/..."}),
			"latitude": forms.NumberInput(attrs={"class": "form-input", "step": "0.000001", "readonly": "readonly"}),
			"longitude": forms.NumberInput(attrs={"class": "form-input", "step": "0.000001", "readonly": "readonly"}),
			"poster": forms.ClearableFileInput(attrs={"class": "form-input"}),
			"youtube_link": forms.URLInput(attrs={"class": "form-input", "placeholder": "https://www.youtube.com/..."}),
			"additional_info": forms.Textarea(attrs={"class": "form-textarea", "rows": 4}),
		}
		labels = {
			"title": "Meeting Title / Meeting Name *",
			"description": "Meeting Description *",
			"start_date": "Meeting Starting Date *",
			"end_date": "Meeting Ending Date *",
			"organizer_name": "Meeting Organizer Name *",
			"estimated_attendance": "Estimated Number of People Attending *",
			"organizer_phone": "Meeting Organizer Phone Number (Not displayed to public) *",
			"address": "Meeting Address / Location *",
			"district": "District *",
			"state": "State *",
			"google_map_location": "Google Map Location (Optional)",
			"poster": "Meeting Poster Image Upload",
			"youtube_link": "YouTube Channel Link",
			"additional_info": "Additional Information",
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["meeting_type"].required = False
		self.fields["meeting_type"].choices = [("", "సెలెక్ట్ సమావేశాలు టైపు")] + list(MEETING_TYPE_CHOICES)
		self.fields["denomination"].required = False
		self.fields["denomination"].choices = [("", "సెలెక్ట్ డినామినేషన్")] + list(DENOMINATION_CHOICES)
		self.fields["ministry"].required = False
		self.fields["ministry"].choices = [("", "Select Ministry")] + list(MINISTRY_CHOICES)
		self.fields["district"].choices = [("", "సెలెక్ట్ జిల్లా")] + list(DISTRICT_CHOICES)

	def clean(self):
		cleaned_data = super().clean()
		start_date = cleaned_data.get("start_date")
		end_date = cleaned_data.get("end_date")
		if start_date and end_date and end_date < start_date:
			raise ValidationError("Meeting Ending Date cannot be before Meeting Starting Date.")
		return cleaned_data


class MeetingFilterForm(forms.Form):
	meeting_type = forms.ChoiceField(
		required=False,
		choices=[("", "సెలెక్ట్ సమావేశాలు టైపు")] + list(MEETING_TYPE_CHOICES),
		widget=forms.Select(attrs={"class": "form-select"}),
	)
	denomination = forms.ChoiceField(
		required=False,
		choices=[("", "సెలెక్ట్ డినామినేషన్")] + list(DENOMINATION_CHOICES),
		widget=forms.Select(attrs={"class": "form-select"}),
	)
	ministry = forms.ChoiceField(
		required=False,
		choices=[("", "Select Ministry")] + list(MINISTRY_CHOICES),
		widget=forms.Select(attrs={"class": "form-select"}),
	)
	date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date", "class": "form-input"}))
	district = forms.ChoiceField(
		required=False,
		choices=[("", "సెలెక్ట్ జిల్లా")] + list(DISTRICT_CHOICES),
		widget=forms.Select(attrs={"class": "form-select"}),
	)
	city_area = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-input", "placeholder": "City / Area"}))
	mandal = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-input", "placeholder": "Mandal"}))
	village = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-input", "placeholder": "Village"}))
