### Configuration
In prior lessons, and in
[Introduction to Celery](
https://docs.celeryq.dev/en/stable/getting-started/introduction.html)
the celery configuration and tasks are placed in the same file `tasks.py`. In begin of
learning process it is ok, and even better. But in real life when you are familiar with
celery `app` object, celery configuration, and tasks should be separated to better manage
you whole (web)application. The "flow" is `configuration` -> `app` -> `tasks`.
(sidenotes: 1. according to https://12factor.net your (web)application's configuration
should be stored and passed to application via environment variables; 2. usually
in python projects configuration is accessible via python variables; 3. sidenote
1 and 2 can be merged).

### Code
```python
# celery_config.py
# variable names are important!
broker_url = "redis://redis:6379/0"
result_backend = "rpc://"

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'
enable_utc = True
```

```python
# celery_app.py
from celery import Celery
app = Celery()
app.config_from_object('celery_config')
```

```python
# tasks.py
from celery_app import app

@app.task
def add(x, y):
    return x + y

# <other-tasks>
```

### Run
As previously run whole `docker-compose up --build`. Then start new session with
`docker-compose exec celery_service ipython`. You can run following code to see that
configuration are applied to app:

```python
from celery_app import app

print(app.conf.broker_url)
print(app.conf.result_backend)
print(app.conf.task_serializer)
print(app.conf.result_serializer)
print(app.conf.accept_content)
print(app.conf.timezone)
print(app.conf.enable_utc)
```

And start simple task:
```python
from tasks import sleep_task
sleep_task.apply_async(args=(5,))
```

### FAQ
**Q: What can I configure in celery**

A: A lot of things, for details see
https://docs.celeryq.dev/en/stable/userguide/configuration.html

### Homework
1. In docker-compose switch to rabbitmq. Then reconfigure celery to use rabbitmq.
2. Extract configuration to environment variables, and in `celery_config.py` read them.
