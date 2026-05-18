"""
Account submission forms matching the reference repository structure.
These are forms for Account menu items that logged-in users can submit.
"""
from django import forms
from jobs.models import Job
from businesses.models import Business
from institutes.models import Institute
from incidents.models import Incident
from core.models import Prayer
from directory.models import DISTRICT_CHOICES, STATE_CHOICES
from meetings.models import Meeting


class StyledFormMixin:
	"""Automatically apply CSS classes to form fields."""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			widget = field.widget
			css_class = "form-input"
			if isinstance(widget, forms.CheckboxInput):
				css_class = "form-checkbox"
			elif isinstance(widget, forms.Select):
				css_class = "form-select"
			elif isinstance(widget, forms.Textarea):
				css_class = "form-textarea"
			widget.attrs["class"] = f"{widget.attrs.get('class', '')} {css_class}".strip()


# ============================================================================
# ACCOUNT MENU FORMS (11 Forms matching reference repo)
# ============================================================================

class ChurchTimingsForm(StyledFormMixin, forms.Form):
	"""Form for submitting church service timings."""
	service_name = forms.CharField(
		max_length=100,
		label="Service Name",
		widget=forms.TextInput(attrs={"placeholder": "e.g., Sunday Morning Service"})
	)
	day = forms.ChoiceField(
		choices=[
			("sunday", "Sunday"),
			("monday", "Monday"),
			("tuesday", "Tuesday"),
			("wednesday", "Wednesday"),
			("thursday", "Thursday"),
			("friday", "Friday"),
			("saturday", "Saturday"),
		],
		label="Day of Week"
	)
	time_start = forms.TimeField(
		widget=forms.TimeInput(attrs={"type": "time"}),
		label="Start Time"
	)
	time_end = forms.TimeField(
		widget=forms.TimeInput(attrs={"type": "time"}),
		label="End Time"
	)
	description = forms.CharField(
		max_length=500,
		required=False,
		widget=forms.Textarea(attrs={"rows": 3}),
		label="Description"
	)


class MeetingsForm(StyledFormMixin, forms.ModelForm):
	"""Form for submitting meeting/event information."""
	class Meta:
		model = Meeting
		fields = [
			"meeting_type", "speaker_one", "speaker_two", "speaker_three", "speaker_four",
			"from_date", "to_date", "from_time", "to_time",
			"image", "description", "address", "city_area",
			"facebook_link", "youtube_link",
			"district", "state",
			"organization_name", "contact_phone", "event_phone",
			"expected_attendance", "denomination"
		]
		widgets = {
			"description": forms.Textarea(attrs={"rows": 4}),
			"from_date": forms.DateInput(attrs={"type": "date"}),
			"to_date": forms.DateInput(attrs={"type": "date"}),
			"from_time": forms.TimeInput(attrs={"type": "time"}),
			"to_time": forms.TimeInput(attrs={"type": "time"}),
			"address": forms.Textarea(attrs={"rows": 2}),
		}
		labels = {
			"meeting_type": "Type of Meeting",
			"speaker_one": "Speaker 1 Name",
			"speaker_two": "Speaker 2 Name (Optional)",
			"speaker_three": "Speaker 3 Name (Optional)",
			"speaker_four": "Speaker 4 Name (Optional)",
			"from_date": "From Date",
			"to_date": "To Date",
			"from_time": "From Time",
			"to_time": "To Time",
			"image": "Event Image",
			"description": "Event Description",
			"address": "Event Address",
			"city_area": "City/Area",
			"facebook_link": "Facebook Link (Optional)",
			"youtube_link": "YouTube Link (Optional)",
			"district": "District",
			"state": "State",
			"organization_name": "Organization Name",
			"contact_phone": "Contact Phone",
			"event_phone": "Event Phone",
			"expected_attendance": "Expected Attendance",
			"denomination": "Denomination",
		}


class JobsForm(StyledFormMixin, forms.ModelForm):
	"""Form for posting job requirements."""
	class Meta:
		model = Job
		fields = [
			"title", "description", "experience_level", "education_level",
			"salary_min", "salary_max", "city_area", "district", "state",
			"company_name", "company_email", "company_phone", "company_website",
			"skills_required", "benefits", "application_link", "deadline"
		]
		widgets = {
			"description": forms.Textarea(attrs={"rows": 4}),
			"skills_required": forms.Textarea(attrs={"rows": 2}),
			"benefits": forms.Textarea(attrs={"rows": 2}),
			"deadline": forms.DateInput(attrs={"type": "date"}),
		}
		labels = {
			"title": "Job Title",
			"description": "Job Description",
			"experience_level": "Experience Required",
			"education_level": "Education Level",
			"salary_min": "Minimum Salary",
			"salary_max": "Maximum Salary",
			"city_area": "City/Area",
			"district": "District",
			"state": "State",
			"company_name": "Company Name",
			"company_email": "Company Email",
			"company_phone": "Company Phone",
			"company_website": "Company Website",
			"skills_required": "Required Skills",
			"benefits": "Benefits Offered",
			"application_link": "Application Link",
			"deadline": "Application Deadline",
		}


class BusinessForm(StyledFormMixin, forms.ModelForm):
	"""Form for posting business information."""
	class Meta:
		model = Business
		fields = [
			"business_name", "description", "category", "business_type",
			"owner_name", "owner_email", "owner_phone",
			"district", "state", "city_area", "address",
			"website", "established_year", "services_offered"
		]
		widgets = {
			"description": forms.Textarea(attrs={"rows": 4}),
			"address": forms.Textarea(attrs={"rows": 2}),
			"services_offered": forms.Textarea(attrs={"rows": 2}),
		}
		labels = {
			"business_name": "Business Name",
			"description": "Business Description",
			"category": "Business Category",
			"business_type": "Business Type",
			"owner_name": "Owner Name",
			"owner_email": "Owner Email",
			"owner_phone": "Owner Phone",
			"district": "District",
			"state": "State",
			"city_area": "City/Area",
			"address": "Business Address",
			"website": "Website",
			"established_year": "Year Established",
			"services_offered": "Services Offered",
		}


class InstituteForm(StyledFormMixin, forms.ModelForm):
	"""Form for posting institute/educational information."""
	class Meta:
		model = Institute
		fields = [
			"institute_name", "description", "institute_type", "category",
			"principal_name", "principal_email", "principal_phone",
			"district", "state", "city_area", "address",
			"website", "established_year", "student_count",
			"degrees_offered", "specializations", "affiliation"
		]
		widgets = {
			"description": forms.Textarea(attrs={"rows": 4}),
			"address": forms.Textarea(attrs={"rows": 2}),
			"specializations": forms.Textarea(attrs={"rows": 2}),
		}
		labels = {
			"institute_name": "Institute Name",
			"description": "Description",
			"institute_type": "Institute Type",
			"category": "Category",
			"principal_name": "Principal/Director Name",
			"principal_email": "Principal Email",
			"principal_phone": "Principal Phone",
			"district": "District",
			"state": "State",
			"city_area": "City/Area",
			"address": "Address",
			"website": "Website",
			"established_year": "Year Established",
			"student_count": "Number of Students",
			"degrees_offered": "Degrees Offered",
			"specializations": "Specializations",
			"affiliation": "Board/University Affiliation",
		}


class AttacksForm(StyledFormMixin, forms.ModelForm):
	"""Form for reporting incidents/attacks."""
	class Meta:
		model = Incident
		fields = [
			"title", "description", "incident_type", "severity", "incident_date",
			"victim_name", "victim_phone", "victim_email",
			"attacker_name", "attacker_phone",
			"district", "state", "city_area", "location_description",
			"fir_number", "evidence_details"
		]
		widgets = {
			"description": forms.Textarea(attrs={"rows": 4}),
			"location_description": forms.Textarea(attrs={"rows": 2}),
			"evidence_details": forms.Textarea(attrs={"rows": 2}),
			"incident_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
		}
		labels = {
			"title": "Incident Title",
			"description": "Incident Description",
			"incident_type": "Type of Incident",
			"severity": "Severity Level",
			"incident_date": "Date & Time of Incident",
			"victim_name": "Victim Name",
			"victim_phone": "Victim Phone",
			"victim_email": "Victim Email",
			"attacker_name": "Attacker Name (if known)",
			"attacker_phone": "Attacker Phone (if known)",
			"district": "District",
			"state": "State",
			"city_area": "City/Area",
			"location_description": "Location Details",
			"fir_number": "FIR Number (if registered)",
			"evidence_details": "Evidence Details",
		}


class PrayerForm(StyledFormMixin, forms.ModelForm):
	"""Form for submitting prayer requests."""
	class Meta:
		model = Prayer
		fields = ["title", "description", "category", "is_public"]
		widgets = {
			"description": forms.Textarea(attrs={"rows": 4}),
		}
		labels = {
			"title": "Prayer Request Title",
			"description": "Prayer Request Description",
			"category": "Category",
			"is_public": "Make this prayer public (visible to community)",
		}


class AdsForm(StyledFormMixin, forms.Form):
	"""Form for posting advertisements."""
	title = forms.CharField(
		max_length=200,
		label="Advertisement Title"
	)
	ad_type = forms.ChoiceField(
		choices=[
			("service", "Service"),
			("product", "Product"),
			("event", "Event"),
			("announcement", "Announcement"),
		],
		label="Advertisement Type"
	)
	description = forms.CharField(
		widget=forms.Textarea(attrs={"rows": 4}),
		label="Advertisement Description"
	)
	image_url = forms.URLField(
		required=False,
		label="Image URL (Optional)"
	)
	contact_phone = forms.CharField(
		max_length=20,
		label="Contact Phone"
	)


class ProfileForm(StyledFormMixin, forms.Form):
	"""Form for viewing and editing profile."""
	# This is typically handled by profile-specific forms
	# This placeholder shows structure matching reference repo
	pass


class LeadersForm(StyledFormMixin, forms.Form):
	"""Form for registering as a leader."""
	name = forms.CharField(max_length=200, label="Full Name")
	email = forms.EmailField(label="Email Address")
	phone = forms.CharField(max_length=20, label="Phone Number")
	experience = forms.CharField(
		widget=forms.Textarea(attrs={"rows": 4}),
		label="Leadership Experience"
	)
	areas_of_interest = forms.CharField(
		widget=forms.Textarea(attrs={"rows": 3}),
		label="Areas of Interest"
	)


# ============================================================================
# SERVICES MENU FORMS (Search/List views - these handle filtering)
# ============================================================================

class InstitutesSearchForm(StyledFormMixin, forms.Form):
	"""Form for searching institutes."""
	institute_name = forms.CharField(
		max_length=200,
		required=False,
		label="Institute Name (Optional)"
	)
	institute_type = forms.ChoiceField(
		required=False,
		label="Institute Type (Optional)",
		choices=[("", "All Types")] + [
			("school", "School"),
			("college", "College"),
			("university", "University"),
			("seminary", "Seminary"),
			("training_center", "Training Center"),
		]
	)
	district = forms.ChoiceField(
		required=False,
		label="District (Optional)",
		choices=[("", "All Districts")] + DISTRICT_CHOICES
	)


class MarriagesSearchForm(StyledFormMixin, forms.Form):
	"""Form for searching marriage profiles."""
	gender = forms.ChoiceField(
		required=False,
		label="Gender (Optional)",
		choices=[("", "All"), ("male", "Male"), ("female", "Female")]
	)
	district = forms.ChoiceField(
		required=False,
		label="District (Optional)",
		choices=[("", "All Districts")] + DISTRICT_CHOICES
	)
	age_min = forms.IntegerField(required=False, label="Minimum Age (Optional)")
	age_max = forms.IntegerField(required=False, label="Maximum Age (Optional)")


class JobsSearchForm(StyledFormMixin, forms.Form):
	"""Form for searching jobs."""
	job_title = forms.CharField(
		max_length=200,
		required=False,
		label="Job Title (Optional)"
	)
	district = forms.ChoiceField(
		required=False,
		label="District (Optional)",
		choices=[("", "All Districts")] + DISTRICT_CHOICES
	)
	job_type = forms.ChoiceField(
		required=False,
		label="Job Type (Optional)",
		choices=[("", "All Types"), ("full_time", "Full Time"), ("part_time", "Part Time"), ("contract", "Contract")]
	)


class HelpSearchForm(StyledFormMixin, forms.Form):
	"""Form for searching for help/assistance."""
	help_category = forms.ChoiceField(
		choices=[
			("financial", "Financial Help"),
			("medical", "Medical Assistance"),
			("counseling", "Counseling"),
			("legal", "Legal Aid"),
			("other", "Other"),
		],
		label="Type of Help Needed"
	)
	district = forms.ChoiceField(
		required=False,
		label="District (Optional)",
		choices=[("", "All Districts")] + DISTRICT_CHOICES
	)


class NewsSearchForm(StyledFormMixin, forms.Form):
	"""Form for searching/browsing news."""
	category = forms.ChoiceField(
		required=False,
		label="Category (Optional)",
		choices=[("", "All Categories"), ("christian", "Christian News"), ("community", "Community News"), ("events", "Events")]
	)


class BusinessSearchForm(StyledFormMixin, forms.Form):
	"""Form for searching businesses."""
	business_name = forms.CharField(
		max_length=200,
		required=False,
		label="Business Name (Optional)"
	)
	business_type = forms.CharField(
		max_length=100,
		required=False,
		label="Business Type (Optional)"
	)
	district = forms.ChoiceField(
		required=False,
		label="District (Optional)",
		choices=[("", "All Districts")] + DISTRICT_CHOICES
	)


class WingsSearchForm(StyledFormMixin, forms.Form):
	"""Form for searching JBAC organizational information."""
	wing_type = forms.CharField(
		max_length=100,
		required=False,
		label="Wing Type (Optional)"
	)


class OrganizationSearchForm(StyledFormMixin, forms.Form):
	"""Form for searching Christian organizations."""
	organization_name = forms.CharField(
		max_length=200,
		required=False,
		label="Organization Name (Optional)"
	)
	organization_type = forms.ChoiceField(
		required=False,
		label="Organization Type (Optional)",
		choices=[
			("", "All Types"),
			("church", "Church"),
			("ministry", "Ministry"),
			("ngo", "NGO"),
			("association", "Association"),
		]
	)
	district = forms.ChoiceField(
		required=False,
		label="District (Optional)",
		choices=[("", "All Districts")] + DISTRICT_CHOICES
	)
