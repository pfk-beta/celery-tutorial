from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_example.settings")

app = Celery("django_example")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
