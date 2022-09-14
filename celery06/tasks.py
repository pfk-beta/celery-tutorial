from celery import Celery
import django
import os
import random
import string

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_example.settings")
django.setup()

from django.contrib.auth.models import User

app = Celery(
    "django_example", broker="pyamqp://guest@rabbitmq//", backend="redis://redis:6379/0"
)


def random_name(length):
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))


@app.task
def create_a_lot_of_users(no_users):
    for _ in range(no_users):
        username = random_name(10)
        User.objects.create(username=username)
