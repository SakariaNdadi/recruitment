from django.db import models
from django.urls import reverse
from apps.company.models import Position
from django.conf import settings
from apps.accounts.models import Profile
from django.utils import timezone
from django.core.exceptions import ValidationError

class JobCompetency(models.Model):
    employee = models.ForeignKey(
        Profile, related_name="jcp", on_delete=models.SET_NULL, null=True
    )
    position = models.ForeignKey(
        Position, related_name="job_competency", on_delete=models.CASCADE
    )
    is_published = models.BooleanField(default=False)
    deadline = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Job Competency Profile"
        verbose_name_plural = "Job Competency Profiles"

    def clean(self):
        super().clean()
        if self.deadline <= timezone.now():
            self.is_published = False

    def __str__(self):
        return self.position.title

    def get_absolute_url(self):
        return reverse("employee_competency_profile_detail", kwargs={"pk": self.pk})
    
    @classmethod
    def create_new_history(cls, employee, position):
        current_year = timezone.now().year
        existing_history = cls.objects.filter(employee=employee, position=position, created__year=current_year).first()
        if not existing_history:
            new_history = cls.objects.create(employee=employee, position=position)
            return new_history
        return existing_history


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.CharField(max_length=250)
    category = models.ForeignKey(
        Category, related_name="questions", on_delete=models.CASCADE
    )
    job_competency = models.ForeignKey(
        JobCompetency, related_name="questions", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.text


class CompetencyAnswer(models.Model):
    question = models.ForeignKey(
        Question, related_name="answer", on_delete=models.CASCADE
    )
    employee_answer = models.PositiveSmallIntegerField(null=True, blank=True)
    supervisor_answer = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.question.text} - {self.question.job_competency.position.title}"
    
    def save(self, *args, **kwargs):
        if self.question.job_competency.position.line_manager:
            self.supervisor_answer = self.question.job_competency.position.line_manager.jcp.filter(is_published=True).first()
        super().save(*args, **kwargs)
