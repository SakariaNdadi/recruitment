from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse
from django.core.exceptions import ValidationError
from apps.company.models import Position
from .fields import OrderField
from django_ckeditor_5.fields import CKEditor5Field

User = get_user_model()

class Subject(models.Model):
    title = models.CharField(max_length=200)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

class Course(models.Model):
    owner = models.ForeignKey(User, related_name="course_created", on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, related_name="courses", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    outline = CKEditor5Field()
    duration = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name="Duration (days)"
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("course_detail", args=[self.pk])


class Module(models.Model):
    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=["course"])

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.order}. {self.title}"

    def get_absolute_url(self):
        return reverse("module_detail", args=[self.pk])


class Content(models.Model):
    module = models.ForeignKey(
        Module, related_name="contents", on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={"model__in": ("text", "video", "image", "file")},
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "object_id")
    order = OrderField(blank=True, for_fields=["module"])

    class Meta:
        ordering = ["order"]


class ItemBase(models.Model):
    owner = models.ForeignKey(
        User, related_name="%(class)s_related", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("item_detail", args=[self.pk])


class Text(ItemBase):
    content = CKEditor5Field()


class File(ItemBase):
    file = models.FileField(upload_to="files")


class Image(ItemBase):
    file = models.FileField(upload_to="images")


class Video(ItemBase):
    url = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to="videos")


# **************************************************************************************************


class CourseRequest(models.Model):
    class STATUS(models.TextChoices):
        APPROVE = "approved", "Approved"
        DECLINE = "declined", "Declined"
        SUBMIT = "submitted", "Submitted"

    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS.choices)
    line_manager = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    reason = CKEditor5Field()
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee} - {self.course}"

    def get_absolute_url(self):
        return reverse("course_request_detail", args=[self.pk])


class Training(models.Model):
    trainer = models.ForeignKey(
        User, related_name="trainings", on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course, related_name="trainings", on_delete=models.CASCADE
    )
    trainees = models.ManyToManyField(User, related_name="training_attendees")
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=100)
    # attendance = models.ManyToManyField(User, related_name="training_attendance", through='AttendanceRecord')

    def __str__(self):
        return f"{self.course.title} Training"

    def get_absolute_url(self):
        return reverse("training_detail", args=[self.pk])

    # def mark_attendance(self, trainee, present=True):
    #     """
    #     Method to mark attendance for a trainee.
    #     """
    #     if trainee not in self.trainees.all():
    #         raise ValidationError("This user is not registered for the training.")
    #     attendance_record, created = AttendanceRecord.objects.get_or_create(training=self, trainee=trainee)
    #     attendance_record.present = present
    #     attendance_record.save()

    def save(self, *args, **kwargs):
        """
        Override the save method to prevent modifications once the training is set.
        """
        if self.pk:  # Check if the instance already exists (update operation)
            raise ValidationError(
                "Modifications to a training instance are not allowed once it is set."
            )
        super().save(*args, **kwargs)


# class AttendanceRecord(models.Model):
#     training = models.ForeignKey(Training, on_delete=models.CASCADE)
#     trainee = models.ForeignKey(User, on_delete=models.CASCADE)
#     present = models.BooleanField(default=False)

#     class Meta:
#         unique_together = ('training', 'trainee')

#     def __str__(self):
#         return f"{self.trainee.profile.first_name} {self.trainee.profile.last_name} - {self.training}"
