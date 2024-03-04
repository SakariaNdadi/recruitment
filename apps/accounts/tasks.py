from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model
from celery import shared_task
from .models import Profile
from apps.skills_audit.models import JobCompetency

User = get_user_model()

@shared_task
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if instance.email.endswith("@telecom.na"):
        instance.profile.user_type = "staff"
        instance.profile.save()


@shared_task
@receiver(post_save, sender=Profile)
def create_job_competency(sender, instance, created, **kwargs):
    if instance.is_created:
        position = instance.position
        if position and instance.user_type in ["staff", "manager", "chief"]:
            JobCompetency.objects.create(employee=instance, position=position)