from django import forms
from utils.file import validate_file
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime
from .models import Vacancy, Application, Interview, Bursary, BursaryApplication


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


class ApplicationCreateForm(forms.ModelForm):
    document = forms.FileField(
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
        fields = (
            "cover_letter",
            "document",
        )

    def clean(self):
        cleaned_data = super().clean()
        submission_date = cleaned_data.get("submission_date")
        vacancy_deadline = cleaned_data.get("vacancy.deadline")

        # Check if the submission date is after the vacancy deadline
        if submission_date and submission_date > vacancy_deadline:
            raise ValidationError(
                "Application cannot be submitted after the vacancy deadline."
            )

        return cleaned_data


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
