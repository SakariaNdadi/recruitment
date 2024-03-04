from django.db import models
from django.contrib.auth import get_user_model
from django_ckeditor_5.fields import CKEditor5Field


User = get_user_model()


class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # description = models.TextField(blank=True, null=True)
    description = CKEditor5Field(blank=True, null=True)
    chief = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="chief",
    )

    def __str__(self):
        return self.name


class Division(models.Model):
    title = models.CharField(max_length=50, unique=True)
    # description = models.TextField(blank=True, null=True)
    description = CKEditor5Field(blank=True, null=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="divisions"
    )
    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="manager",
    )

    class Meta:
        ordering = [
            "title",
        ]
        indexes = [
            models.Index(fields=["title"]),
        ]

    def __str__(self):
        return self.title


class Qualification(models.Model):
    class Type(models.TextChoices):
        NTA1 = "nta1", "NTA Level 1"
        NTA2 = "nta2", "NTA Level 2"
        NTA3 = "nta3", "NTA Level 3"
        NTA4 = "nta4", "NTA Level 4"
        NTA5 = "nta5", "NTA Level 5"
        NTA6 = "nta6", "NTA Level 6"
        CERTIFICATE = "certificate", "Certificate"
        DIPLOMA = "diploma", "Diploma"
        BACHELORS = "bachelors", "Bachelors"
        HONOURS = "honours", "Honours"
        MASTERS = "masters", "Masters"
        PHD = "phd", "PHD"

    type = models.CharField(max_length=15, choices=Type.choices)
    title = models.CharField(max_length=50)

    def __str__(self):
        capitalized_type = self.type.capitalize()
        return f"{capitalized_type} in {self.title}"

class Certification(models.Model):
    title = models.CharField(max_length=50)
    level = models.CharField(max_length=50)
    institution_name = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Position(models.Model):
    class JobGrade(models.TextChoices):
        A1 = "a1", "A1"
        A2 = "a2", "A2"
        A3 = "a3", "A3"
        A4 = "a4", "A4"
        A5 = "a5", "A5"
        AU = "au", "AU"
        B1 = "b1", "B1"
        B2 = "b2", "B2"
        B3 = "b3", "B3"
        B4 = "b4", "B4"
        B5 = "b5", "B5"
        BU = "bu", "BU"
        C1 = "c1", "C1"
        C2 = "c2", "C2"
        C3 = "c3", "C3"
        C4 = "c4", "C4"
        C5 = "c5", "C5"
        D1 = "d1", "D1"
        D2 = "d2", "D2"
        D3 = "d3", "D3"
        D4 = "d4", "D4"
        D5 = "d5", "D5"
        DU = "du", "DU"

    title = models.CharField(max_length=50)
    key_purpose = CKEditor5Field(blank=True, null=True)
    key_result_areas = CKEditor5Field(blank=True, null=True)
    key_knowledge = CKEditor5Field(blank=True, null=True)
    personality_requirements = CKEditor5Field(blank=True, null=True)
    experience = CKEditor5Field(blank=True, null=True)
    job_grade = models.CharField(max_length=2, choices=JobGrade.choices)
    division = models.ForeignKey(
        Division, on_delete=models.CASCADE, related_name="position"
    )
    qualification = models.ManyToManyField(
        Qualification, related_name="position", symmetrical=False
    )
    line_manager = models.ForeignKey(
        "Position",
        related_name="subordinates",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = [
            "title",
        ]
        indexes = [
            models.Index(fields=["title"]),
        ]

    def __str__(self):
        return self.title
