from django import forms
from jobs.models import Job, JobCategory, JOB_TYPE_CHOICES, EXPERIENCE_LEVEL_CHOICES
from businesses.models import Business, BusinessCategory, BUSINESS_TYPE_CHOICES
from institutes.models import Institute, InstituteCategory, INSTITUTE_TYPE_CHOICES
from incidents.models import Incident, INCIDENT_TYPE_CHOICES, SEVERITY_CHOICES
from core.models import Prayer, PRAYER_CATEGORY_CHOICES
from directory.models import DISTRICT_CHOICES, STATE_CHOICES


class StyledFormMixin:
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


class JobSubmissionForm(StyledFormMixin, forms.ModelForm):
	class Meta:
		model = Job
		fields = [
			"title", "description", "category", "job_type", "experience_level",
			"education_level", "district", "state", "city_area",
			"salary_min", "salary_max", "company_name", "company_email",
			"company_phone", "company_website", "skills_required", "benefits",
			"application_link", "application_email", "deadline"
		]
		widgets = {
			"description": forms.Textarea(attrs={"rows": 4}),
			"skills_required": forms.Textarea(attrs={"rows": 2}),
			"benefits": forms.Textarea(attrs={"rows": 2}),
			"deadline": forms.DateTimeInput(attrs={"type": "datetime-local"}),
		}
		labels = {
			"title": "Job Title",
			"description": "Job Description",
			"category": "Job Category",
			"job_type": "Job Type",
			"experience_level": "Experience Level Required",
			"education_level": "Education Level",
			"district": "District",
			"state": "State",
			"city_area": "City/Area",
			"salary_min": "Minimum Salary",
			"salary_max": "Maximum Salary",
			"company_name": "Company Name",
			"company_email": "Company Email",
			"company_phone": "Company Phone",
			"company_website": "Company Website",
			"skills_required": "Required Skills (comma-separated)",
			"benefits": "Benefits Offered",
			"application_link": "Application Link",
			"application_email": "Application Email",
			"deadline": "Application Deadline",
		}


class BusinessSubmissionForm(StyledFormMixin, forms.ModelForm):
	class Meta:
		model = Business
		fields = [
			"business_name", "description", "category", "business_type",
			"district", "state", "city_area", "address",
			"latitude", "longitude",
			"owner_name", "owner_email", "owner_phone",
			"website", "established_year",
			"logo_url", "image_url",
			"services_offered", "working_hours"
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
			"district": "District",
			"state": "State",
			"city_area": "City/Area",
			"address": "Business Address",
			"latitude": "Latitude (for map)",
			"longitude": "Longitude (for map)",
			"owner_name": "Owner Name",
			"owner_email": "Owner Email",
			"owner_phone": "Owner Phone",
			"website": "Website URL",
			"established_year": "Year Established",
			"logo_url": "Logo URL",
			"image_url": "Business Image URL",
			"services_offered": "Services Offered",
			"working_hours": "Working Hours",
		}


class InstituteSubmissionForm(StyledFormMixin, forms.ModelForm):
	class Meta:
		model = Institute
		fields = [
			"institute_name", "description", "institute_type", "category",
			"district", "state", "city_area", "address",
			"latitude", "longitude",
			"principal_name", "principal_email", "principal_phone",
			"website", "established_year", "student_count",
			"degrees_offered", "specializations",
			"image_url", "affiliation"
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
			"district": "District",
			"state": "State",
			"city_area": "City/Area",
			"address": "Address",
			"latitude": "Latitude",
			"longitude": "Longitude",
			"principal_name": "Principal/Director Name",
			"principal_email": "Principal Email",
			"principal_phone": "Principal Phone",
			"website": "Website",
			"established_year": "Year Established",
			"student_count": "Number of Students",
			"degrees_offered": "Degrees Offered",
			"specializations": "Specializations",
			"image_url": "Image URL",
			"affiliation": "Board/University Affiliation",
		}


class IncidentReportForm(StyledFormMixin, forms.ModelForm):
	class Meta:
		model = Incident
		fields = [
			"title", "description", "incident_type", "severity",
			"incident_date",
			"district", "state", "location",
			"latitude", "longitude",
			"victim_name", "victim_phone", "victim_email",
			"witnesses",
			"fir_number", "police_station",
			"evidence_attachments"
		]
		widgets = {
			"description": forms.Textarea(attrs={"rows": 4}),
			"incident_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
			"witnesses": forms.Textarea(attrs={"rows": 2}),
			"evidence_attachments": forms.Textarea(attrs={"rows": 2}),
		}
		labels = {
			"title": "Incident Title",
			"description": "Detailed Description",
			"incident_type": "Type of Incident",
			"severity": "Severity Level",
			"incident_date": "Date & Time of Incident",
			"district": "District",
			"state": "State",
			"location": "Incident Location",
			"latitude": "Latitude",
			"longitude": "Longitude",
			"victim_name": "Victim Name (Optional)",
			"victim_phone": "Victim Phone (Optional)",
			"victim_email": "Victim Email (Optional)",
			"witnesses": "Witness Information (Optional)",
			"fir_number": "FIR Number (if filed)",
			"police_station": "Police Station",
			"evidence_attachments": "Evidence/Document URLs (Optional)",
		}


class PrayerSubmissionForm(StyledFormMixin, forms.ModelForm):
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
			"is_public": "Make this prayer request public",
		}
