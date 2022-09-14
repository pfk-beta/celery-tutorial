## Few changes - first experiments

When you want to experiment with celery, it is comfortable to have autoreload feature.
I mean when you create new task, or redefine previous you need to restart worker, so
it knows changes. Autoreload will restart worker whenever you change something. When we
have such functionality we can put our worker into docker-compose definition, so we
don't need to run worker in separate shell session. To play with celery I have created
some extra simple tasks - more arithmetic, and simple wait.

#### Autoreload
There are few ways to achieve autoreload feature, in general use dedicated tool or
create your own implementation. Everyone has pros and cons. There are a few dedicated
tools, and many-many implementations.
Implementations:
1. `--autoreload` options in celery - it is removed since celery 4.0.
2. when you use django and celery you can use `autoreload` from `django.utils`.
3. `watchdog` pypi library
4. `watchfiles` pypi library

### Run
Similarly to previous lession, start docker-compose with following command:
`docker-compose up --build`. It will start redis server, celery worker with autoreload
and celery_service to run example commands. In next shell run command
`docker-compose exec celery_service ipython` to interact with celery.

Example code to run with celery
```python
from tasks import add, mul, div, sleep_task
sleep_task(3)  # 1.
add.delay(4, 4)  # 2.
mul.delay(4, 5)  # 3.
sleep_task.delay(3)  # 4.
res = add.delay(4, 5)  # 5.
print(res.get())  # 6.
```
When play with celery, it's good practice to look what is going inside worker, to see
which tasks are received from message broker. It is good way to learn how it is working.
As you can see tasks, can be call as regular function `1.` - it is not executed by worker,
but by your shell, i.e. celery_service. `2.` and `3.` are typicall usage of celery tasks.
In our case `add` and `mul` are tiny tasks, which takes about 0.001s to execute. So we
don't see that task is running in background. But `4.` is running time consuming task -
waiting - and we can see that we are not waiting for this task, we see results of next
tiny task. The same situation we can see in worker output, we see that `add` task is
succeed, then `sleep_task` is succeed.


### FAQ
**Q: Can I change something?**

A: Whatever you want, e.g. service names, add new tasks, reconfigure celery, rename task,
add extra prints, call whatever tasks that you create, create infinite tasks...

**Q: What is `res` variable in `6.`**

A: TLDR; object representing task. According to documentation it is AsyncResult (
https://docs.celeryq.dev/en/stable/reference/celery.app.task.html#celery.app.task.Task.delay),
according to concurrent programming paradigm it is future promise (
https://en.wikipedia.org/wiki/Futures_and_promises).

**Q: is there other ways of calling tasks**

A: Have you seen examples of calling tasks in python projects? Have you seen celery
documentation? Yes, there are few ways to call celery tasks, e.g. apply_async, using
signatures.

### Homework
1. Can you create another worker in docker-compose?
2. Can you change message broker?
