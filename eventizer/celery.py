from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eventizer.settings")
app = Celery("eventizer")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
