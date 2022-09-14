from celery import Celery

app = Celery("tasks", broker="pyamqp://guest@rabbitmq//", backend="rpc://")


@app.task
def add(x, y):
    return x + y
