from django import forms
from utils.file import validate_file
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime
from .models import (
    Vacancy,
    Application,
    Interview,
    Bursary,
    BursaryApplication,
    Application,
)
from apps.company.models import Qualification
from phonenumber_field.formfields import PhoneNumberField
from django_recaptcha.fields import ReCaptchaField, ReCaptchaV3
from django.utils.translation import gettext_lazy as _


# ******************************************************************************************************
#                                     Custom Fields
# ******************************************************************************************************
class CustomDateTimeField(forms.DateTimeField):
    def validate(self, value):
        super().validate(value)
        if value:
            if not self.is_valid_day(value):
                raise ValidationError(
                    "Interviews must be scheduled on Monday to Friday."
                )
            if not self.is_valid_time(value):
                raise ValidationError(
                    "Interviews must be scheduled between 8 am and 4 pm."
                )

    def is_valid_day(self, value):
        return 1 <= value.weekday() <= 4  # Monday is 0, Sunday is 6

    def is_valid_time(self, value):
        # start_time = timezone.make_aware(
        #     value.replace(hour=8, minute=0, second=0, microsecond=0)
        # )
        # end_time = timezone.make_aware(
        #     value.replace(hour=16, minute=0, second=0, microsecond=0)
        # )
        # return start_time <= value <= end_time
        start_time = value.replace(hour=8, minute=0, second=0, microsecond=0)
        end_time = value.replace(hour=16, minute=0, second=0, microsecond=0)
        return start_time <= value <= end_time


# ******************************************************************************************************
#                                     Vacancy Forms
# ******************************************************************************************************

class VacancyForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"class": "form-control", "type": "datetime-local"}
        )
    )

    class Meta:
        model = Vacancy
        fields = (
            "position",
            "town",
            "deadline",
            "is_published",
            "is_external",
            "remarks",
        )


# ******************************************************************************************************
#                                     Application Forms
# ******************************************************************************************************
class ApplicationCreateForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    qualifications = forms.ModelMultipleChoiceField(
        queryset=Qualification.objects.none(),
        widget=forms.CheckboxSelectMultiple(attrs={}),
        required=True,
        label="Do you have any of the required qualifications?",
    )
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
        required=False,
        widget=forms.NumberInput(
            attrs={
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                "placeholder": "081 234 5678",
            }
        ),
    )
    document = forms.FileField(
        validators=[validate_file],
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400",
                "accept": ".pdf",
            }
        ),
    )
    cv = forms.FileField(
        validators=[validate_file],
        widget=forms.ClearableFileInput(
            attrs={
                "class": "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400",
                "accept": ".pdf",
            }
        ),
    )
    cover_letter = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                "placeholder": "Why should we take you for this position?",
            }
        ),
    )

    class Meta:
        model = Application
        exclude = [
            "user",
            "vacancy",
            "status",
            "remarks",
            "qualifications",
        ]

    def clean(self):
        cleaned_data = super().clean()
        submission_date = cleaned_data.get("submission_date")
        vacancy_deadline = cleaned_data.get("vacancy.deadline")
        date_of_birth = cleaned_data.get("date_of_birth")
        id_number = cleaned_data.get("id_number")
        passport_number = cleaned_data.get("passport_number")
        user = self.user

        if user and hasattr(user, 'is_authenticated'):
            pass
        else:
            # Check if either id_number or passport_number is provided, but not both
            if not id_number and not passport_number:
                raise ValidationError(
                    _("Either ID number or passport number must be provided.")
                )
            if id_number and passport_number:
                raise ValidationError(
                    _("Please provide either ID number or passport number, not both.")
                )

            
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
                    if (
                        id_month != date_month
                        or id_day != date_day
                        or id_year != date_year
                    ):
                        raise ValidationError(
                            {"id_number": [_("ID number does not match date of birth")]}
                        )

        # Check if the submission date is after the vacancy deadline
        if submission_date:
            if submission_date > vacancy_deadline:
                raise ValidationError(
                    _("Application cannot be submitted after the vacancy deadline.")
                )

        return cleaned_data

    def clean_qualifications(self):
        qualifications = self.cleaned_data.get("qualifications")
        if not qualifications:
            raise ValidationError(_("At least one qualification must be selected."))
        return qualifications

    def save(self, commit=True):
        # Save the form instance
        instance = super().save(commit=False)

        if commit:
            instance.save()

            # Extract the qualifications from the cleaned data
            qualifications = self.cleaned_data.get("qualifications")
            if qualifications:
                # Add the selected qualifications to the qualification field
                instance.qualifications.add(*qualifications)

        return instance
    
    def __init__(self, *args, vacancy_instance=None, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if vacancy_instance:
            self.fields["qualifications"].queryset = (
                vacancy_instance.position.qualification.all()
            )
        if user and user.is_authenticated and user.profile.is_created:
            self.exclude_fields_for_authenticated_user()

    def exclude_fields_for_authenticated_user(self):
        self.fields.pop("first_name")
        self.fields.pop("last_name")
        self.fields.pop("email")
        self.fields.pop("nationality")
        self.fields.pop("population_group")
        self.fields.pop("id_number")
        self.fields.pop("passport_number")
        self.fields.pop("gender")
        self.fields.pop("date_of_birth")
        self.fields.pop("primary_contact")
        self.fields.pop("secondary_contact")
        self.fields.pop("cv")


class ApplicationEvaluationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = (
            "remarks",
            "status",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the "Submitted" option from the status field
        self.fields["status"].choices = [
            choice
            for choice in self.fields["status"].choices
            if choice[0] != "submitted"
        ]


# ******************************************************************************************************
#                                     Bursary Forms
# ******************************************************************************************************

class BursaryForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"class": "form-control", "type": "datetime-local"}
        )
    )

    class Meta:
        model = Bursary
        fields = (
            "title",
            "criteria",
            "deadline",
            "is_external",
            "is_published",
        )


class BursaryApplicationForm(forms.ModelForm):
    commencement_date = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )

    class Meta:
        model = BursaryApplication
        fields = (
            "field_of_study",
            "relevancy_to_current_occupation",
            "institute",
            "mode_of_study",
            "mode_of_study_reason",
            "minimum_study_duration",
            "maximum_study_duration",
            "commencement_date",
            "tuition_fees",
            "travel_fees",
            "accommodation_fees",
            "books_fees",
            "other_fees",
            "first_year_total_fees",
            "gross_total_all_years",
        )


# ******************************************************************************************************
#                                     Interview Forms
# ******************************************************************************************************
class InterviewForm(forms.ModelForm):
    application = forms.ModelChoiceField(
        queryset=Application.objects.filter(
            vacancy__deadline__lt=timezone.now(), status="shortlisted"
        ),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Choose Applicant",
    )
    dateTime = CustomDateTimeField(
        widget=forms.DateTimeInput(
            attrs={"class": "form-control", "type": "datetime-local"}
        )
    )

    class Meta:
        model = Interview
        fields = (
            "application",
            "dateTime",
            "description",
            "location",
            "interview_type",
            "duration",
        )

    def clean(self):
        cleaned_data = super().clean()
        application = cleaned_data.get("application")
        date_time = cleaned_data.get("dateTime")
        duration = cleaned_data.get("duration")

        if application and date_time and duration:
            # Check if the day is Monday to Friday
            if date_time.weekday() not in [0, 1, 2, 3, 4]:
                raise ValidationError(
                    "Interviews can only be scheduled between Monday to Friday."
                )

            start_time = date_time
            end_time = start_time + timezone.timedelta(minutes=duration)

            # Check if the time is between 8 am and 5 pm
            if start_time.time() < datetime.time(
                8, 0
            ) or end_time.time() > datetime.time(17, 0):
                raise ValidationError(
                    "Interviews can only be scheduled between 8 am and 5 pm."
                )

            # Check if there's an existing interview with overlapping time period
            existing_interview = Interview.objects.filter(
                application=application,
                dateTime__lt=end_time,
                dateTime__gt=start_time,
            )

            if existing_interview:
                raise ValidationError(
                    "An interview already exists at the same time or overlaps in duration."
                )

            # Check if the interview is scheduled within the next 2 days
            current_time = timezone.now()
            if start_time < current_time + timezone.timedelta(days=2):
                raise ValidationError(
                    "Interviews cannot be scheduled within the next 2 days."
                )

        return cleaned_data