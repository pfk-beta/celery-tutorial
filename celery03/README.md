### More workers, more tasks, more options

In real world, you may have many users of you (web)application, you may have a lot
of data. To process these data you will need more processing power, and to accomplish
it, you will need more workers - we have configured one extra celery worker in docker
compose file. Additionally in worker command I have added sleep command, because worker
starts before rabbitmq is ready. If you are seeing error message about connection
problem you may try to increase this sleep, or switch to redis. If you see warning
message, that docker-compose's deploy is not working, then you may need to upgrade
docker-compose command in your system.

### Run

#### Check basic information about task
```python
from tasks import sleep_task
res = sleep_task.delay(15)  # 1.
print(res.id)  # 2.
print(res.task_id)
print(res.status)
print(res.ready())  # 3.

import time
print("Waiting in this shell session for task complete...")
time.sleep(20)  # 4.
print(res)  # 5.
print(res.ready())  # 6.
print(res.get())  # 7.
print(res.ready())  # 8.
print(res.status)  # 9.
print(res.result)  # 10.
```
`1.` - call task.
`2.` - print task id - it is unique id.
`3.` - check if task is finished.
`4.` - sleep 15 seconds in this shell, to check task results.
`5.` - print ApplyAsync, its repr is just task_id.
`6.` - check if task is ready. Something is wrong here. Task should be finished.
And ready tells that it is not finished.
`7.` - we call `get()` to update AsyncResult, and to get returned value
`8.` - now we are ready after update information
`9.` - status
`10.` - task returned value is stored in `result` property.
This properties and methods are described in documentation
https://docs.celeryq.dev/en/stable/reference/celery.result.html
As you may notice calling `.get()` method will synchronize asynchronous task. In
documentation there are few extra and interesting methods of AsyncResult.

#### More sophisticated calling tasks
These methods are described in user guide in celery documentation
https://docs.celeryq.dev/en/stable/userguide/calling.html#guide-calling
```python
# using apply_async and specify arguments in *args
from tasks import sleep_task
sleep_task.apply_async(args=(5,)).get()
```

```python
# using apply_async and specify arguments in *kwargs
from tasks import sleep_task
sleep_task.apply_async(kwargs={'i': 6})
```

```python
# you can mix args, and kwargs
from tasks import add
add.apply_async(args=(1,), kwargs={'y': 6})
```

```python
# what if override?
from tasks import add
add.apply_async(args=(1, 4), kwargs={'x': 1, 'y': 6})
```

```python
# you can run your task in a few seconds
from tasks import div
res = div.apply_async(args=(20, 10), countdown=3)
print(res.get())
```

```python
# you can run your task in specified timestamp
from tasks import div
from datetime import datetime, timedelta
div.apply_async(args=(10, 2), eta=datetime.now() + timedelta(hours=10))
```

Another methods of calling tasks, is by using signatures. Signatures are mostly used when
you want control workflow of tasks.
```python
from celery import signature
task_sig = signature('tasks.div', args=(20, 10))
task_sig.delay()
```

```python
from tasks import div
task_sig = div.s(100, 5)
task_sig.delay()
```

#### Play with celery cli
Remember command to start worker. So worker is one of many subcommands of celery. To see
other you can see in documentation https://docs.celeryq.dev/en/stable/reference/cli.html
or type `celery` in shell. Each of subcommands has help section, e.g. `celery amqp --help`.
When you call these commands, you probably need to specify `--app` or `-A` parameter.
These subcommands are highly related with `app` object, in our cases defined in
`tasks.py`, e.g. `celery -A tasks control revoke` is `app.control.revoke`.

```shell
# print stats of each worker
celery -A tasks inspect stats
```
If you didn't make homework of previous lessons, don't worry. But this homework
is valuable - take a look.

### FAQ
**Q: Can I cancel called task?**

A: you can revoke your task, see details
 https://docs.celeryq.dev/en/stable/reference/celery.result.html#celery.result.AsyncResult.revoke


### Homework
1. Try to achieve following statuses, not neccesary for the same task: PENDING,
STARTED, FAILURE, SUCCESS.
2. Wait for task by using AsyncResult's dedicated method.
3. Call report subcommand.
4. Revoke task with celery command.
5. Print graph of workers with celery command.
6. Ping your workers with celery command.
7. Print reports of your workers with celery command.
8. Visit https://docs.celeryq.dev/en/stable/userguide/monitoring.html
