from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_user_profile(sender, instance, created, **kwargs):
    if instance.email.endswith("@telecom.na"):
        instance.profile.user_type = "staff"
        instance.profile.save()


# @receiver(post_save, sender=Profile)
# def create_job_competency(sender, instance, created, **kwargs):
#     if instance.is_created:
#         position = instance.position
#         if position and instance.user_type in ["temp", "staff", "manager", "chief"]:
#             JobCompetency.objects.create(employee=instance, position=position)