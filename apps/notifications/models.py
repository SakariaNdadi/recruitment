from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
User = get_user_model()

class Notification(models.Model):
    class TYPES(models.TextChoices):
        INFO = "info"
        WARNING = "warning"
        ERROR = "error"
    
    class ACTIONS(models.TextChoices):
        CREATED = "created"
        UPDATED = "updated"
        DELETED = "deleted"

    user = models.ManyToManyField(User, related_name="notifications")
    message = models.CharField(max_length=500)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField()
    link = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=50, choices=TYPES.choices)
    action = models.CharField(max_length=50, choices=ACTIONS.choices)

    def get_absolute_url(self):
        return reverse("notification_detail", args=[self.pk])
    