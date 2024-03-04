from django.db import models
from apps.company.models import Position
from django.urls import reverse
from utils.file import user_file_upload_path, application_file_upload_path
from apps.accounts.models import Qualification
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
import datetime
from djmoney.models.fields import MoneyField
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
import pycountry
from django.db.models import UniqueConstraint
from django_ckeditor_5.fields import CKEditor5Field

User = get_user_model()


class Region(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Town(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="towns")
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    position = models.ForeignKey(
        Position, on_delete=models.CASCADE, related_name="position"
    )
    town = models.ForeignKey(Town, on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    is_published = models.BooleanField(default=False)
    is_external = models.BooleanField(default=False)
    remarks = CKEditor5Field(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]
        verbose_name_plural = "Vacancies"

    def __str__(self):
        return self.position.title

    def get_absolute_url(self):
        return reverse("vacancy_detail", args=[self.id])


class Application(models.Model):
    COUNTRY_CHOICES = [
        (country.alpha_2.lower(), country.name) for country in pycountry.countries
    ]

    class PopulationGroup(models.TextChoices):
        RACIALLY_ADVANTAGED = "ra", "Racially Advantaged"
        RACIALLY_DISADVANTAGED = "rd", "Racially Disadvantaged"

    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"

    class Status(models.TextChoices):
        SUBMITTED = "submitted", "Submitted"
        SHORTLISTED = "shortlisted", "Shortlisted"
        REJECTED = "rejected", "Rejected"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="applications"
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    nationality = models.CharField(max_length=50, choices=COUNTRY_CHOICES, default="na")
    population_group = models.CharField(max_length=50, choices=PopulationGroup.choices)
    id_number = models.PositiveBigIntegerField(blank=True, null=True)
    passport_number = models.CharField(max_length=9, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    date_of_birth = models.DateField()
    primary_contact = PhoneNumberField(region="NA")
    secondary_contact = PhoneNumberField(blank=True, null=True)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.SUBMITTED
    )
    cover_letter = CKEditor5Field(blank=True, null=True)
    cv = models.FileField(
        upload_to=application_file_upload_path,
        validators=[FileExtensionValidator(["pdf"])],
    )
    document = models.FileField(
        upload_to=application_file_upload_path,
        validators=[FileExtensionValidator(["pdf"])],
        blank=True,
        null=True,
    )
    qualifications = models.ManyToManyField(Qualification)
    remarks = CKEditor5Field(blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["vacancy", "user"],
                name="unique_vacancy_user",
            ),
            UniqueConstraint(
                fields=["vacancy", "id_number"],
                name="unique_vacancy_id_number",
            ),
            UniqueConstraint(
                fields=["vacancy", "passport_number"],
                name="unique_vacancy_passport_number",
            ),
        ]

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if self.user and self.user.is_authenticated:
            self.first_name = self.user.profile.first_name
            self.last_name = self.user.profile.last_name
            self.email = self.user.email
            self.id_number = self.user.profile.id_number
            self.gender = self.user.profile.gender
            self.date_of_birth = self.user.profile.date_of_birth
            self.primary_contact = self.user.profile.primary_contact
            self.secondary_contact = self.user.profile.secondary_contact
            self.cv = self.user.profile.cv

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("application_detail", args=[self.pk])


class Interview(models.Model):
    class Status(models.TextChoices):
        SET = "set", "Set"
        ACCEPT = "accept", "Accept"
        REJECT = "reject", "Reject"
        SCHEDULED = "scheduled", "Scheduled"
        ONGOING = "ongoing", "Ongoing"
        COMPLETED = "completed", "Completed"
        RESCHEDULED = "rescheduled", "Rescheduled"

    class InterviewType(models.TextChoices):
        IN_PERSON = "in_person", "In-Person"
        TEST = "test", "Test"
        PHONE = "phone", "Phone"
        VIDEO = "video", "Video"
        ONLINE = "online", "Online"

    class Location(models.TextChoices):
        ONLINE = "online", "Microsoft Teams"
        TRAINING = "training", "Training Centre, Voigst Street"
        HEAD = "headOffice", "Head Office, Independence Avenue"

    application = models.ForeignKey(
        Application,
        related_name="interviews",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    dateTime = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SET)
    description = CKEditor5Field(blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, choices=Location.choices)
    interview_type = models.CharField(
        max_length=20, choices=InterviewType.choices, default=InterviewType.IN_PERSON
    )
    duration = models.PositiveIntegerField(default=30)  # Duration in minutes
    reschedule_reason = CKEditor5Field(blank=True)
    reschedule_date = models.DateTimeField(null=True, blank=True)
    rejection_reasons = CKEditor5Field(blank=True)

    def __str__(self):
        return self.application

    def get_absolute_url(self):
        return reverse("interview_detail", args=[self.pk])

    def clean(self):
        cleaned_data = super().clean()
        application = self.application
        date_time = self.dateTime
        duration = self.duration

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
            existing_interview = (
                Interview.objects.filter(
                    application=application,
                    dateTime__lt=end_time,
                    dateTime__gt=start_time,
                )
                .exclude(pk=self.pk)
                .first()
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


class Bursary(models.Model):
    title = models.CharField(max_length=200)
    criteria = CKEditor5Field()
    is_external = models.BooleanField(default=False)
    deadline = models.DateTimeField()
    is_published = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Bursarie"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("bursary_detail", args=[self.pk])


class BursaryApplication(models.Model):
    class STATUS_TYPE(models.TextChoices):
        SUBMITTED = "submitted", "Submitted"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    class MODE_OF_STUDY(models.TextChoices):
        FULL_TIME = "full_time", "Full Time"
        PART_TIME = "part_time", "Part Time"

    bursary = models.ForeignKey(
        Bursary, related_name="bursary", on_delete=models.CASCADE
    )
    applicant = models.ForeignKey(
        User, related_name="applicant", on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=20, choices=STATUS_TYPE.choices, default=STATUS_TYPE.SUBMITTED
    )
    # PARTICULARS RELATING TO THE COURSE OF STUDY
    field_of_study = models.CharField(max_length=150)
    relevancy_to_current_occupation = CKEditor5Field()
    institute = models.CharField(max_length=100)
    mode_of_study = models.CharField(max_length=20, choices=MODE_OF_STUDY.choices)
    mode_of_study_reason = CKEditor5Field()
    minimum_study_duration = models.PositiveSmallIntegerField()
    maximum_study_duration = models.PositiveSmallIntegerField()
    commencement_date = models.DateField()
    # COST ESTIMATE
    tuition_fees = MoneyField(max_digits=14, decimal_places=2, default_currency="NAD")
    travel_fees = MoneyField(max_digits=14, decimal_places=2, default_currency="NAD")
    accommodation_fees = MoneyField(
        max_digits=14, decimal_places=2, default_currency="NAD"
    )
    books_fees = MoneyField(max_digits=14, decimal_places=2, default_currency="NAD")
    other_fees = MoneyField(max_digits=14, decimal_places=2, default_currency="NAD")
    other_fees_specification = models.CharField(max_length=200)
    first_year_total_fees = MoneyField(
        max_digits=14, decimal_places=2, default_currency="NAD"
    )
    gross_total_all_years = MoneyField(
        max_digits=14, decimal_places=2, default_currency="NAD"
    )
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bursary}"
