### Types of workload

Every project has own type of workload to be computed by celery. We can image simple
scenarios:
1. We have (web)app, in which almost all request are processed by (web)server. But
sometimes request takes much longer time(e.g. generate report, export/import data,
generally process large portion of data), and we want to avoid timeout responses,
nor locking (web)client. So these longer requests are delegated to celery workers -
(web)app notifies only about background task, finished or failed task.

2. We have (web)app, in which we are using of some kind resources, e.g. CPU, GPU or
external device. We have also many users, whose jobs requires resources. During the day
there are more jobs, that at night.

### Monitoring
In official documentation there are a lot of information about monitoring your celery
stuff. You can do it manually by calling `celery inspect` commands. You can implement
your own service for monitoring. You can also grab ready solution - one of most known
is flower. Flower beyond monitoring has also few functionality to control workers.
Recent flower versions has not graph charts.
Sidenotes:
 - when you open worker in flower, you may see `Unknown worker` message, then you need
 to refresh page
 - regular rabbitmq image has no management plugin, to properly configure flower, you
 need to use image version with `-management` suffix.
 - to configure flower to manage rabbitmq, you need to specify `broker_api`, it may
 looks like `broker_api=http://guest@rabbitmq:15672/api/vhost` - 15672 default port
 which can be changed in rabbitmq's configuration.


### Code
Let's create simple but time and CPU consuming task. This is good example how not to
write programs, i.e. avoid nested loops:
```python
from django_example.celery import app

@app.task
def nested_loops(x, y, z):
    sum_value = 0
    for i in range(x):
        for j in range(y):
            for k in range(z):
                sum_value += i + j + k
    return sum_value
```

### Run
As usual, run docker compose `docker-compose up --build`. Then in seconds shell session
`docker-compose exec django ipython`. We could spawn only one task, to see how much time
it needs to finish job. You can experiment with different arguments, but be careful.
Start from low values, e.g. 20, 100. Then try to increase values. On my computer
500, 500, 500 takes 13-17 seconds and occupies one thread at 100\%.

```python
from coreapp.tasks import nested_loops
from time import sleep
for _ in range(10):
    nested_loops.delay(500, 500, 500)
    sleep(10)
```

### FAQ

### Homework
