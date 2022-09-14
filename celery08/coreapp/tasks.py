from django_example.celery import app


@app.task
def nested_loops(x, y, z):
    sum_value = 0
    for i in range(x):
        for j in range(y):
            for k in range(z):
                sum_value += i + j + k
    return sum_value
