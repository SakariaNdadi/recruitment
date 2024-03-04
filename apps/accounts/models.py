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
from django_ckeditor_5.fields import CKEditor5Field

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
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    user_type = models.CharField(
        max_length=10, choices=UserType.choices, default=UserType.STAFF
    )
    nationality = models.CharField(max_length=50, choices=COUNTRY_CHOICES, default="na")
    population_group = models.CharField(
        max_length=50, choices=PopulationGroup.choices, null=True, blank=True
    )
    id_number = models.PositiveBigIntegerField(null=True, unique=True)
    gender = models.CharField(
        max_length=10, choices=Gender.choices, null=True
    )
    date_of_birth = models.DateField(null=True)
    primary_contact = PhoneNumberField(region="NA", null=True)
    secondary_contact = PhoneNumberField(blank=True, null=True)

    # employee details
    position = models.ForeignKey(
        Position, on_delete=models.SET_NULL, null=True
    )
    employee_id = models.PositiveBigIntegerField(null=True)
    office_contact = PhoneNumberField(region="NA", blank=True, null=True)
    call_center_number = models.PositiveIntegerField(null=True)
    appointed_date = models.DateField(null=True)

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
