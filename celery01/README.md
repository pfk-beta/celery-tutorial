## First steps with celery

Let's start with very basic example, based on very basic example from celery
`Getting started`.


### Quick review about docker
This is content of docker-compose of this lesson:
```yaml
version: "3.3"
services:
  celery_service:
    build:
      context: .
      dockerfile: Dockerfile
    tty: true
    depends_on:
      - rabbitmq
    volumes:
      - .:/app:z

  rabbitmq:
    image: rabbitmq:3
```

There are 2 services. celery_service and rabbitmq. Both services are managing only one
docker container. Rabbitmq is message broker required by celery to properly work.
Celery first is container for presenting lesson. Container is being build from
Dockerfile - inside it we are using base python image, then we are installing required
libraries. We also mount files from this folder to celery_fist container. (sidenode:
I haved named `celery_service` to be easier distinguish for learners, in real life
key service is redundant and can be skipped)

### Code
Example code from celery page is:
```python
from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def add(x, y):
    return x + y
```

In this example authors assumes rabbitmq is installed in the localhost. We have
rabbitmq inside docker-compose, without exposed ports. And we will run examples
inside docker-compose envirment. Service names can be used and host names. So. So just
replace localhost with rabbitmq. Let's write these to file `tasks.py`. But what we
write here exactly? First line - import celery, next line configure celery,
usually `app` variable. Next lines are task defintion - decorator and function
to decorate. I have added one extra parameter to configuration called bakend,
it is described later in celery documentation - it is used to pass results of tasks.


### Run
Run docker-compose with following command: `docker-compose up --build`. Then you need
to run 2 shell sessions:
1. `docker-compose exec celery_service celery -A tasks worker --loglevel=INFO`
2. `docker-compose exec celery_service ipython`
Up and exec commands you need to run in folder where is docker-compose file. Inside
2nd shell type:
```python
from tasks import add
add.delay(4, 4)
res = add.delay(9, 5)
print(res.get())
```

See what is going in shell, where you have run worker. In my session I can see
following messages:
```logs
[2022-09-08 19:33:18,651: INFO/MainProcess] Connected to amqp://guest:**@rabbitmq:5672//
[2022-09-08 19:33:18,657: INFO/MainProcess] mingle: searching for neighbors
[2022-09-08 19:33:19,699: INFO/MainProcess] mingle: all alone
[2022-09-08 19:33:19,720: INFO/MainProcess] celery@e02c8210761c ready.
[2022-09-08 19:33:23,730: INFO/MainProcess] Task tasks.add[f98b7aa8-eb43-424f-8b91-b62eaf6ec09a] received
[2022-09-08 19:33:23,745: INFO/ForkPoolWorker-2] Task tasks.add[f98b7aa8-eb43-424f-8b91-b62eaf6ec09a] succeeded in 0.014267109000684286s: 8
[2022-09-08 19:34:09,091: INFO/MainProcess] Task tasks.add[f51ea0c9-ca98-436d-a665-0c0503e33c4b] received
[2022-09-08 19:34:09,092: INFO/ForkPoolWorker-2] Task tasks.add[f51ea0c9-ca98-436d-a665-0c0503e33c4b] succeeded in 0.000683008999658341s: 8
[2022-09-08 19:34:09,093: INFO/MainProcess] Task tasks.add[9d2e2bef-3acc-42a4-abf1-9e20c0840d14] received
[2022-09-08 19:34:09,094: INFO/ForkPoolWorker-2] Task tasks.add[9d2e2bef-3acc-42a4-abf1-9e20c0840d14] succeeded in 0.0005123669998283
```

Have you see what is printed in docker-compose in rabbitmq output:
```logs
rabbitmq_1      | 2022-09-08 19:33:18.649211+00:00 [info] <0.941.0> accepting AMQP connection <0.941.0> (172.23.0.3:53816 -> 172.23.0.2:5672)
rabbitmq_1      | 2022-09-08 19:33:18.651076+00:00 [info] <0.941.0> connection <0.941.0> (172.23.0.3:53816 -> 172.23.0.2:5672): user 'guest' authenticated and granted access to vhost '/'
rabbitmq_1      | 2022-09-08 19:33:18.653409+00:00 [info] <0.949.0> accepting AMQP connection <0.949.0> (172.23.0.3:53818 -> 172.23.0.2:5672)
rabbitmq_1      | 2022-09-08 19:33:18.655037+00:00 [info] <0.949.0> connection <0.949.0> (172.23.0.3:53818 -> 172.23.0.2:5672): user 'guest' authenticated and granted access to vhost '/'
rabbitmq_1      | 2022-09-08 19:33:18.665766+00:00 [info] <0.971.0> accepting AMQP connection <0.971.0> (172.23.0.3:53820 -> 172.23.0.2:5672)
rabbitmq_1      | 2022-09-08 19:33:18.667554+00:00 [info] <0.971.0> connection <0.971.0> (172.23.0.3:53820 -> 172.23.0.2:5672): user 'guest' authenticated and granted access to vhost '/'
rabbitmq_1      | 2022-09-08 19:33:23.720658+00:00 [info] <0.1007.0> accepting AMQP connection <0.1007.0> (172.23.0.3:53822 -> 172.23.0.2:5672)
```

### Cleanup
Run command `docker-compose down` will close containers, remove network. But
images and volume still be there. If you know little docker you can remove image,
and volume.

### FAQ

**Q: Can I change something?**

A: Whatever you want, e.g. service names, add new tasks, reconfigure celery.


### Homework
1. What is ip address of my services inside docker network?
2. Change logging level of celery worker
3. Use different backend for celery
4. Use older image version of rabbitmq
