from django.db import models
from django.core.exceptions import ValidationError
from utils.file import user_file_upload_path
from apps.company.models import Division, Position
from django.urls import reverse
from apps.company.models import Qualification
from django.core.validators import FileExtensionValidator
from phonenumber_field.modelfields import PhoneNumberField
import pycountry
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    COUNTRY_CHOICES = [
        (country.alpha_2.lower(), country.name) for country in pycountry.countries
    ]

    class PopulationGroup(models.TextChoices):
        RACIALLY_ADVANTAGED = "ra", "Racially Advantaged"
        RACIALLY_DISADVANTAGED = "rd", "Racially Disadvantaged"

    class UserType(models.TextChoices):
        ADMIN = "admin", "Admin"
        APPLICANT = "applicant", "Applicant"
        CHIEF = "chief", "Chief"
        MANAGER = "manager", "Manager"
        SUPERVISOR = "supervisor", "Supervisor"
        STAFF = "staff", "Staff"
        TEMP = "temp", "Temp/Intern"

    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"

    # basic details
    user = models.OneToOneField(
        User,
        primary_key=True,
        related_name="profile",
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    user_type = models.CharField(
        max_length=10, choices=UserType.choices, default=UserType.APPLICANT
    )
    nationality = models.CharField(max_length=50, choices=COUNTRY_CHOICES, default="na")
    population_group = models.CharField(
        max_length=50, choices=PopulationGroup.choices, null=True, blank=True
    )
    id_number = models.PositiveBigIntegerField(blank=True, null=True, unique=True)
    gender = models.CharField(
        max_length=10, choices=Gender.choices, blank=True, null=True
    )
    date_of_birth = models.DateField(blank=True, null=True)
    primary_contact = PhoneNumberField(region="NA", blank=True, null=True)
    secondary_contact = PhoneNumberField(region="NA", blank=True, null=True)

    # employee details
    position = models.ForeignKey(
        Position, on_delete=models.SET_NULL, null=True, blank=True
    )
    employee_id = models.PositiveBigIntegerField(blank=True, null=True)
    call_center_number = models.PositiveIntegerField(blank=True, null=True)
    appointed_date = models.DateField(null=True, blank=True)
    postal_address = models.TextField(null=True, blank=True)

    # social platforms
    linkedin = models.URLField(blank=True, null=True)
    picture = models.ImageField(
        upload_to=user_file_upload_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["jpg", "png", "jpeg"])],
    )
    cv = models.FileField(
        upload_to=user_file_upload_path, validators=[FileExtensionValidator(["pdf"])]
    )
    is_created = models.BooleanField(default=False)

    # dates
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-user"]
        indexes = [
            models.Index(fields=["-user"]),
            models.Index(fields=["employee_id"]),
            models.Index(fields=["id_number"]),
        ]

    def clean(self):
        if self.id_number and self.date_of_birth:
            try:
                self.id_number = int(self.id_number)
            except ValueError:
                raise ValidationError(
                    {"id_number": [("ID number must be a valid number")]}
                )

            id_str = str(self.id_number)

            # Validate the length of id_number
            if len(id_str) != 11:
                raise ValidationError(
                    {"id_number": [("ID number must be 11 digits long")]}
                )

            # Extract year, month, and day from the ID number
            id_year = int(id_str[:2])
            id_month = int(id_str[2:4])
            id_day = int(id_str[4:6])

            if self.date_of_birth:
                date_month = self.date_of_birth.month
                date_day = self.date_of_birth.day
                date_year = (
                    self.date_of_birth.year % 100
                )  # Extract last two digits of the year

                # Compare the extracted values
                if id_month != date_month or id_day != date_day or id_year != date_year:
                    raise ValidationError(
                        {"id_number": [("ID number does not match date of birth")]}
                    )

        return super().clean()

    def __str__(self):
        return f"{self.user.email}"

    def get_absolute_url(self):
        return reverse("profile_detail", args=[str(self.user.id)])


class Experience(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="experience"
    )
    job_title = models.CharField(max_length=50)
    job_description = models.TextField()
    company_name = models.CharField(max_length=50)
    employment_type = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    employment_status = models.BooleanField(default=False)
    industry = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.job_title

    def get_absolute_url(self):
        return reverse("experience_detail", args=[self.id])


class Education(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="education"
    )
    institution_name = models.CharField(max_length=20)
    qualification = models.ForeignKey(Qualification, on_delete=models.CASCADE)
    obtained_date = models.DateField()
    file = models.FileField(
        upload_to=user_file_upload_path, validators=[FileExtensionValidator(["pdf"])]
    )

    def __str__(self):
        return self.qualification.title

    def get_absolute_url(self):
        return reverse("qualification_detail", args=[self.id])


class Certification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="certification"
    )
    title = models.CharField(max_length=50)
    institution_name = models.CharField(max_length=50)
    obtained_date = models.DateField()
    validity = models.PositiveSmallIntegerField()
    file = models.FileField(
        upload_to=user_file_upload_path, validators=[FileExtensionValidator(["pdf"])]
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("certification_detail", args=[self.id])
