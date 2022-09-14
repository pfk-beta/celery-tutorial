from celery_app import app


@app.task
def f(x):
    return -2 * (x + 7) ** 2 * (x + 3) ** 3 * (x - 1) ** 4 * (x - 3) ** 5 * (x - 6) ** 2
