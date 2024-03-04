from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import Question, CompetencyAnswer

@receiver(post_save, sender=Question)
def create_competency_answer(sender, instance, created, **kwargs):
    if created:
        CompetencyAnswer.objects.create(question=instance)

# Connect the signal
post_save.connect(create_competency_answer, sender=Question)

@receiver(post_delete, sender=Question)
def delete_competency_answer(sender, instance, **kwargs):
    CompetencyAnswer.objects.filter(question=instance).delete()

# Connect the signal for deletion
post_delete.connect(delete_competency_answer, sender=Question)