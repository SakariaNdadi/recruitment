from django import forms
from utils.file import validate_file
from allauth.account.forms import SignupForm
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from .models import Experience, Education, Certification, Profile
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3
from allauth.account.forms import LoginForm, SignupForm
from django.utils import timezone


class CustomTextInput(forms.TextInput):
    def render(self, name, value, attrs=None, **kwargs):
        if "disabled" in attrs and attrs["disabled"]:
            attrs["class"] = "your-custom-class"
        return super().render(name, value, attrs, **kwargs)


class ProfileUpdateBaseForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    date_of_birth = forms.DateField(
        label="Date of Birth",
        disabled=True,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    id_number = forms.IntegerField(disabled=True, label="National ID Number")
    primary_contact = PhoneNumberField(
        region="NA",
        widget=forms.NumberInput(
            attrs={
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                "placeholder": "081 234 5678",
            }
        ),
    )
    secondary_contact = PhoneNumberField(
        region="NA",
        widget=forms.NumberInput(
            attrs={
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                "placeholder": "081 234 5678",
            }
        ),
        required=False,
    )
    gender = forms.CharField(disabled=True)
    population_group = forms.CharField(disabled=True)
    linkedin = forms.URLField(
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "your-linkedin-url", "type": "url"}
        ),
    )
    cv = forms.FileField(
        label="CV",
        validators=[validate_file],
        widget=forms.ClearableFileInput(
            attrs={"class": "form-control-file", "accept": ".pdf"}
        ),
    )

    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "id_number",
            "date_of_birth",
            "primary_contact",
            "secondary_contact",
            "gender",
            "population_group",
            "postal_address",
            "linkedin",
            "cv",
        )


class AdminUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "id_number",
            "employee_id",
            "appointed_date",
            "primary_contact",
            "secondary_contact",
            "gender",
            "population_group",
            "date_of_birth",
            "linkedin",
            "cv",
            "picture",
            "position",
            "call_center_number",
        )


class ApplicantUpdateForm(ProfileUpdateBaseForm):
    pass


class EmployeeUpdateForm(ProfileUpdateBaseForm):
    position = forms.ChoiceField(disabled=True, label="Job Title")
    employee_id = forms.IntegerField(disabled=True, label="Employee ID")
    call_center_number = forms.IntegerField(disabled=True, label="Call Centre Number")
    appointed_date = forms.CharField(disabled=True)
    picture = forms.FileField(
        required=False,
        validators=[FileExtensionValidator(["jpg", "png", "jpeg"])],
        widget=forms.ClearableFileInput(
            attrs={
                "class": "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400",
                "accept": [".png", ".jpg", ".jpeg"],
            }
        ),
    )
    cv = forms.FileField(
        label="CV",
        validators=[validate_file],
        widget=forms.ClearableFileInput(
            attrs={
                "class": "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400",
                "accept": ".pdf",
            }
        ),
    )

    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "id_number",
            "date_of_birth",
            "primary_contact",
            "secondary_contact",
            "gender",
            "population_group",
            "employee_id",
            "appointed_date",
            "call_center_number",
            "position",
            "picture",
            "cv",
        )


class ProfileCreateBaseForm(forms.ModelForm):
    GENDER_CHOICES = [
        (None, "Select your Gender"),  # The empty option is added to force selection
        ("male", "Male"),
        ("female", "Female"),
    ]
    POPULATION_GROUP_CHOICES = [
        (
            None,
            "Select the Population Group you belong to",
        ),  # The empty option is added to force selection
        ("ra", "Racially Advantaged"),
        ("rd", "Racially Disadvantaged"),
    ]
    first_name = forms.CharField()
    last_name = forms.CharField()
    id_number = forms.IntegerField(min_value=0, max_value=99999999999)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    primary_contact = PhoneNumberField(
        region="NA",
        widget=forms.NumberInput(
            attrs={
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                "placeholder": "081 234 5678",
            }
        ),
    )
    secondary_contact = PhoneNumberField(
        region="NA",
        required=False,
        widget=forms.NumberInput(
            attrs={
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                "placeholder": "081 234 5678",
            }
        ),
    )
    gender = forms.ChoiceField(required=True, choices=GENDER_CHOICES)
    population_group = forms.ChoiceField(
        required=True, choices=POPULATION_GROUP_CHOICES
    )
    postal_address = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))
    linkedin = forms.URLField(
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "your-linkedin-url", "type": "url"}
        ),
    )
    cv = forms.FileField(
        label="CV",
        validators=[validate_file],
        widget=forms.ClearableFileInput(
            attrs={
                "class": "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400",
                "accept": ".pdf",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        id_number = cleaned_data.get("id_number")
        date_of_birth = cleaned_data.get("date_of_birth")

        if id_number and date_of_birth:
            try:
                id_number = int(id_number)
            except ValueError:
                raise ValidationError(
                    {"id_number": [_("ID number must be a valid number")]}
                )

            id_str = str(id_number)

            # Validate the length of id_number
            if len(id_str) != 11:
                raise ValidationError(
                    {"id_number": [_("ID number must be 11 digits long")]}
                )

            # Extract year, month, and day from the ID number
            id_year = int(id_str[:2])
            id_month = int(id_str[2:4])
            id_day = int(id_str[4:6])

            if date_of_birth:
                date_month = date_of_birth.month
                date_day = date_of_birth.day
                date_year = (
                    date_of_birth.year % 100
                )  # Extract last two digits of the year

                # Compare the extracted values
                if id_month != date_month or id_day != date_day or id_year != date_year:
                    raise ValidationError(
                        {"id_number": [_("ID number does not match date of birth")]}
                    )

        return cleaned_data

    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "date_of_birth",
            "id_number",
            "primary_contact",
            "secondary_contact",
            "gender",
            "population_group",
            "postal_address",
            "linkedin",
            "cv",
        )

    def save(self, commit=True):
        # Get the instance but don't save it yet
        profile = super(ProfileCreateBaseForm, self).save(commit=False)

        # Set the 'created' field to the current date and time if it's not set
        if not profile.created:
            profile.created = timezone.now()

        # Save the instance if commit is True
        if commit:
            profile.save()

        return profile


class ApplicantCreateForm(ProfileCreateBaseForm):
    pass


class EmployeeCreateForm(ProfileCreateBaseForm):
    employee_id = forms.IntegerField()
    picture = forms.FileField(
        required=False,
        validators=[FileExtensionValidator(["jpg", "png", "jpeg"])],
        widget=forms.ClearableFileInput(
            attrs={
                "class": "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400",
                "accept": [".png", ".jpg", ".jpeg"],
            }
        ),
    )
    position = forms.ChoiceField(required=True, label="Job Title")

    appointed_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "date_of_birth",
            "id_number",
            "primary_contact",
            "secondary_contact",
            "gender",
            "population_group",
            "linkedin",
            "cv",
            "employee_id",
            "appointed_date",
            "picture",
            "position",
            "call_center_number",
        )


class EducationCreateForm(forms.ModelForm):
    obtained_date = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )
    file = forms.FileField(
        validators=[validate_file],
        widget=forms.ClearableFileInput(
            attrs={"class": "form-control-file", "accept": ".pdf"}
        ),
    )

    class Meta:
        model = Education
        fields = (
            "institution_name",
            "qualification",
            "obtained_date",
            "file",
        )


class ExperienceCreateForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )

    class Meta:
        model = Experience
        fields = (
            "job_title",
            "job_description",
            "company_name",
            "employment_type",
            "location",
            "employment_status",
            "industry",
            "start_date",
            "end_date",
        )


class CertificationCreateForm(forms.ModelForm):
    obtained_date = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )
    file = forms.FileField(
        validators=[validate_file],
        widget=forms.ClearableFileInput(
            attrs={"class": "form-control-file", "accept": ".pdf"}
        ),
    )

    class Meta:
        model = Certification
        fields = (
            "title",
            "institution_name",
            "obtained_date",
            "validity",
            "file",
        )
