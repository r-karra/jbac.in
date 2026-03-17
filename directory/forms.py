from django import forms

from accounts.models import User

from .models import (
    DISTRICT_CHOICES,
    STATE_CHOICES,
    BelieverProfile,
    ChurchProfile,
    OrganizationProfile,
    PastorProfile,
    StudentProfile,
)


DISTRICT_FIELD_CHOICES = [("", "జిల్లా ఎంచుకోండి")] + DISTRICT_CHOICES
STATE_FIELD_CHOICES = [("", "రాష్ట్రం ఎంచుకోండి")] + STATE_CHOICES


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


class BaseRegistrationForm(StyledFormMixin, forms.ModelForm):
    mobile_number = forms.CharField(label="మొబైల్ నంబర్")
    email = forms.EmailField(required=False, label="ఇమెయిల్")
    password1 = forms.CharField(widget=forms.PasswordInput, label="పాస్‌వర్డ్")
    password2 = forms.CharField(widget=forms.PasswordInput, label="పాస్‌వర్డ్ నిర్ధారణ")
    consent = forms.BooleanField(
        label="సమాజ సేవల కోసం JBAC నా వివరాలను సురక్షితంగా నిల్వ చేయడానికి నేను అంగీకరిస్తున్నాను.",
    )

    role_value = None

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data["mobile_number"].strip()
        if User.objects.filter(mobile_number=mobile_number).exists():
            raise forms.ValidationError("ఈ మొబైల్ నంబర్ ఇప్పటికే నమోదైంది.")
        return mobile_number

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("ఈ ఇమెయిల్ చిరునామా ఇప్పటికే ఉపయోగంలో ఉంది.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            self.add_error("password2", "పాస్‌వర్డ్లు సరిపోలలేదు.")
        return cleaned_data

    def get_role_value(self):
        return self.role_value

    def build_user_kwargs(self):
        return {
            "mobile_number": self.cleaned_data["mobile_number"],
            "email": self.cleaned_data.get("email"),
            "password": self.cleaned_data["password1"],
            "role": self.get_role_value(),
            "confidentiality_acknowledged": self.cleaned_data["consent"],
        }

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = User.objects.create_user(**self.build_user_kwargs())
        profile.user = user
        if commit:
            profile.save()
        return profile


class BelieverRegistrationForm(BaseRegistrationForm):
    role_value = User.Role.BELIEVER

    class Meta:
        model = BelieverProfile
        fields = [
            "full_name",
            "gender",
            "whatsapp_number",
            "date_of_birth",
            "life_goal",
            "hobbies",
            "youtube_channel",
            "additional_information",
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "life_goal": forms.Textarea(attrs={"rows": 3}),
            "hobbies": forms.Textarea(attrs={"rows": 3}),
            "additional_information": forms.Textarea(attrs={"rows": 4}),
        }

    def build_user_kwargs(self):
        kwargs = super().build_user_kwargs()
        name_parts = self.cleaned_data["full_name"].split(maxsplit=1)
        kwargs["first_name"] = name_parts[0]
        kwargs["last_name"] = name_parts[1] if len(name_parts) > 1 else ""
        return kwargs


class PastorRegistrationForm(BaseRegistrationForm):
    district = forms.ChoiceField(choices=DISTRICT_FIELD_CHOICES)
    state = forms.ChoiceField(choices=STATE_FIELD_CHOICES, initial="ఆంధ్రప్రదేశ్")
    role_value = User.Role.PASTOR

    class Meta:
        model = PastorProfile
        fields = [
            "pastor_name",
            "gender",
            "church_name",
            "church_address",
            "district",
            "state",
            "latitude",
            "longitude",
            "years_of_ministry",
            "additional_information",
        ]
        widgets = {
            "church_address": forms.Textarea(attrs={"rows": 3}),
            "latitude": forms.NumberInput(attrs={"step": "any"}),
            "longitude": forms.NumberInput(attrs={"step": "any"}),
            "additional_information": forms.Textarea(attrs={"rows": 4}),
        }

    def build_user_kwargs(self):
        kwargs = super().build_user_kwargs()
        name_parts = self.cleaned_data["pastor_name"].split(maxsplit=1)
        kwargs["first_name"] = name_parts[0]
        kwargs["last_name"] = name_parts[1] if len(name_parts) > 1 else ""
        return kwargs


class StudentRegistrationForm(BaseRegistrationForm):
    district = forms.ChoiceField(choices=DISTRICT_FIELD_CHOICES)
    state = forms.ChoiceField(choices=STATE_FIELD_CHOICES, initial="ఆంధ్రప్రదేశ్")
    role_value = User.Role.STUDENT

    class Meta:
        model = StudentProfile
        fields = [
            "student_name",
            "gender",
            "college_name",
            "course",
            "year_of_study",
            "district",
            "state",
        ]

    def build_user_kwargs(self):
        kwargs = super().build_user_kwargs()
        name_parts = self.cleaned_data["student_name"].split(maxsplit=1)
        kwargs["first_name"] = name_parts[0]
        kwargs["last_name"] = name_parts[1] if len(name_parts) > 1 else ""
        return kwargs


class ChurchRegistrationForm(BaseRegistrationForm):
    district = forms.ChoiceField(choices=DISTRICT_FIELD_CHOICES)
    state = forms.ChoiceField(choices=STATE_FIELD_CHOICES, initial="ఆంధ్రప్రదేశ్")
    role_value = User.Role.CHURCH

    class Meta:
        model = ChurchProfile
        fields = [
            "church_name",
            "pastor_name",
            "address",
            "village",
            "district",
            "state",
            "latitude",
            "longitude",
            "year_established",
            "ministry_details",
        ]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
            "latitude": forms.NumberInput(attrs={"step": "any"}),
            "longitude": forms.NumberInput(attrs={"step": "any"}),
            "ministry_details": forms.Textarea(attrs={"rows": 4}),
        }

    def build_user_kwargs(self):
        kwargs = super().build_user_kwargs()
        kwargs["first_name"] = self.cleaned_data["church_name"]
        return kwargs


class OrganizationRegistrationForm(BaseRegistrationForm):
    district = forms.ChoiceField(choices=DISTRICT_FIELD_CHOICES)
    state = forms.ChoiceField(choices=STATE_FIELD_CHOICES, initial="ఆంధ్రప్రదేశ్")
    organization_role = forms.ChoiceField(
        choices=[
            (User.Role.PASTOR_ASSOCIATION, "పాస్టర్స్ అసోసియేషన్"),
            (User.Role.MINISTRY, "మినిస్ట్రీలు"),
            (User.Role.ORGANIZATION, "క్రైస్తవ సంస్థ / కంపెనీ"),
        ],
        label="సంస్థ వర్గం",
    )

    class Meta:
        model = OrganizationProfile
        fields = [
            "organization_name",
            "founder_name",
            "address",
            "district",
            "state",
            "website",
            "ministry_type",
        ]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
        }

    def get_role_value(self):
        return self.cleaned_data["organization_role"]

    def build_user_kwargs(self):
        kwargs = super().build_user_kwargs()
        name_parts = self.cleaned_data["founder_name"].split(maxsplit=1)
        kwargs["first_name"] = name_parts[0]
        kwargs["last_name"] = name_parts[1] if len(name_parts) > 1 else ""
        return kwargs