from django import forms
from django.contrib.auth import authenticate
from django.db.models import Q

from .models import User


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


class LoginForm(StyledFormMixin, forms.Form):
    role = forms.ChoiceField(choices=User.Role.choices, label="విభాగం")
    identifier = forms.CharField(label="మొబైల్ నంబర్ లేదా ఇమెయిల్")
    password = forms.CharField(widget=forms.PasswordInput, label="పాస్‌వర్డ్")

    def __init__(self, *args, request=None, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data.get("identifier")
        password = cleaned_data.get("password")
        role = cleaned_data.get("role")

        if not identifier or not password or not role:
            return cleaned_data

        self.user = authenticate(
            self.request,
            username=identifier,
            password=password,
            role=role,
        )
        if self.user is None:
            raise forms.ValidationError("ఎంచుకున్న విభాగానికి సంబంధించిన ప్రవేశ వివరాలు సరైనవి కావు.")

        return cleaned_data

    def get_user(self):
        return getattr(self, "user", None)


class OTPRequestForm(StyledFormMixin, forms.Form):
    role = forms.ChoiceField(choices=User.Role.choices, label="విభాగం")
    identifier = forms.CharField(label="మొబైల్ నంబర్ లేదా ఇమెయిల్")

    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data.get("identifier", "").strip()
        role = cleaned_data.get("role")
        if not identifier or not role:
            return cleaned_data

        self.user = (
            User.objects.filter(Q(mobile_number=identifier) | Q(email__iexact=identifier), role=role)
            .distinct()
            .first()
        )
        if not self.user:
            raise forms.ValidationError("ఎంచుకున్న విభాగంలో ఈ గుర్తింపుకు ఖాతా కనబడలేదు.")
        return cleaned_data

    def get_user(self):
        return getattr(self, "user", None)


class OTPVerifyForm(StyledFormMixin, forms.Form):
    code = forms.CharField(min_length=6, max_length=6, label="ఒకసారి ఉపయోగించే పాస్‌వర్డ్ (OTP)")