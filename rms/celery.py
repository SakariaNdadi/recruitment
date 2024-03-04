import os
from celery import Celery

# Set the appropriate Django settings module based on the environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rms.settings.base')


app = Celery("rms", hostname="rms")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()