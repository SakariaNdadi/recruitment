from celery import shared_task
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.recruitment.models import Application
from django.contrib.auth import get_user_model
from .models import Notification

User =get_user_model()

@shared_task
@receiver(post_save, sender=Application)
def send_vacancy_application_notification(sender, instance, created, **kwargs):
    if created:
        admin_users = User.objects.filter(profile__user_type="admin")
        message = f"New application submitted by {instance.first_name} {instance.last_name}"
        Notification.objects.create(
            user = admin_users,
            message = message,
            timestamp = instance.submission_date,
            type=Notification.TYPES.INFO,
            action=Notification.ACTIONS.CREATED
        )