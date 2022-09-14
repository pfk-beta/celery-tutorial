### Django integration

From my experience Celery is mostly used with Django. But I think it may be also used
with other framework, or in different setups. We will configure celery only for django.

### Run
Before start: I have turned off(commented out) celery worker service in docker-compose,
because we will create django project, and configure celery in next steps. After few
steps we will turn off celery worker, and we will restart docker-compose. But now we
need to start: `docker-compose up --build`. Then we need to go to django container,
and create example project and first app inside one: `docker-compose exec django bash` -
inside this container startproject `django-admin startproject django_example .`, then start
app `python manage.py startapp polls`. We have empty project, if you stick to suggested
names, then files should be ignored in git - that is intention of this tutorial, in real
life you wouldn't ignore source code. Another issue, files which were created inside
container has permission of root user, if you want to modify them in your text editor/IDE
you need to change their ownership, i.e. ```sudo chown `whoami`: -R * ```. Last issue,
add `polls` app to `INSTALLED_APPS` in `django_example/settings.py`

Now we can uncomment `celery_worker` service in `docker-compose.yaml`. And restart
docker-compose.


### Code
Now it is time for real integration. When I was new to Celery, I was confused about
integration with Django, because it is complex. If you will understand it, it will be
easier to configure it. Let's recall django configuration:

1. When you are doing `import django` - you are importing installed Django library
2. When you are doing `python3 manage.py <some-command>`, under the hood you have set
env variable `DJANGO_SETTINGS_MODULE` - which points your settings configuration, and
somewhere is called `django.setup()` - which do many things: setup db, initialize
apps registry, try to import models etc. `django.setup()` requires env variable
`DJANGO_SETTINGS_MODULE` - more details in documentation:
https://docs.djangoproject.com/en/4.1/ref/applications/#django.setup.
3. When you are doing `from <myapp>.models import <MyModel>`, you are using your models.
But to work properly, somewhere earlier must be called django.setup() - most of the
times it is invisible to you, because it is under-the-hood - e.g. `manage.py runserver`
or `manage.py shell`.

Do you remember lesson 4? The same problem is here, when integrating with Django. You
need to place celery configuration, celery app object and celery tasks. Convention is:
1. place configuration values to django project's settings, i.e. `<project_name>/settings.py`.
2. place celery app object in django project's directory, i.e. `<project_name>/celery.py`.
3. place celery tasks inside django apps' `tasks.py` files, e.g. `polls/tasks.py`.

Side notes:
1. If your project is very simple, you can merge these into one file, e.g. `tasks.py`.
    But you must remember about `django.setup()`.
2. Celery doesn't know about django project until you tell him. So:
    1. if you import app's models inside `celery.py` without calling `django.setup()`,
    you will end up with exception about no apps registry and missing models.
    2. If you call celery tasks only from place, where you have configured django
    (`DJANGO_SETTINGS_MODULE`, and `django.setup()`), then you may import model inside
    your models. (control flow: **django setup** -> **celery task** ->
    **import app's model** -> **task body**).

#### Configure celery
```python
# tasks.py
from celery import Celery
app = Celery(
    "django_example",
    broker="pyamqp://guest@rabbitmq//",
    backend="redis://redis:6379/0")
```

#### Configure django & celery
```python
# tasks.py - the same file
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_example.settings')
django.setup()
```

#### Sample task
```python
# tasks.py - the same file
import random
import string
from django.contrib.auth.models import User

def random_name(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

@app.task
def create_a_lot_of_users(no_users):
    for _ in range(no_users):
        username = random_name(10)
        User.objects.create(username=username)
```

#### Call task
Call `docker-compose exec django bash` in separate shell session. Inside, call
`python3 manage.py migrate` to populate database with migrations. Now you can call one
of 2 commands `ipython` or `python3 manage.py shell` - inside it call:
```python
from tasks import create_a_lot_of_users
res = create_a_lot_of_users.delay(100)
res.get()
```

### FAQ



### Homework
1. In [Section call task](####Call-task) I mention about calling `ipython` or
`python3 manage.py shell`. Which one set up django under the hood?
