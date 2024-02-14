from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from apps.recruitment.models import Vacancy

@receiver(pre_save, sender=Vacancy)
def update_is_published(sender, instance, **kwargs):
    if instance.deadline < timezone.now():
        instance.is_published = False
