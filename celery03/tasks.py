from celery import Celery
import time

app = Celery("tasks", broker="pyamqp://guest@rabbitmq//", backend="rpc://")


@app.task
def add(x, y):
    return x + y


@app.task
def mul(a, b):
    return a * b


@app.task
def div(a, b):
    return a / b


@app.task
def sleep_task(i):
    time.sleep(i)
    return "your turn"
