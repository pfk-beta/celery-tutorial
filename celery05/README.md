### More tasks
Let's say that you want to print math function. Computing value of this function is
computationally demanding, so you will distribute it across your workers.

### Code
```python
from celery_app import app

@app.task
def f(x):
    return -2 * (x + 7)**2 * (x + 3)**3 * (x - 1)**4 * (x - 3)**5 * (x - 6)**2
```

And we want to draw for x from -100 to 100 by 0.1. We can do this in several ways:

#### Very simple
This example is very very simple, we can see loop, in which we spawn task with proper
argument.
```python
from tasks import f

for x in range(-1000, 1000, 1):
    f.delay(x / 10)
```

To print chart, we need to get y values, and knows mapping x -> y. To extend
this example we would like to call `.get()` method, but we don't want to block other
tasks. So we need to save mapping x -> task, then after last task, we check all task
to get mapping task -> y, and finally x -> y.
```python
from tasks import f
x_mapping = dict()

for x in range(-1000, 1000, 1):
    t = f.delay(x / 10)
    x_mapping[x / 10] = t

x_mapping = {x: task.get() for x, task in x_mapping.items()}
```

#### Intermediate

Do you remember signatures from lesson 3? There are required to run more sophisticated
workflows. There are few ways of running multiple tasks. You can run chains, groups,
chords. I encourage you to read details about them in documentation. But here are brief:
 - chain - run one by one tasks, where result of task is passed to next task, and so on.
 - group - run tasks in parrarel
 - chord - run tasks, and then run single task at the end (important note: chord are not
 supported when using RPC backend, the same used in our examples)

```python
# group
from celery import group
from tasks import f

task_list = list()
for x in range(-1000, 1000, 1):
    task_list.append(f.s(x / 10))
g = group(*task_list)
res = g()
y = res.get()
```

### FAQ

### Homework
1. Switch backend to other that RPC (you may need to modify docker-compose).
2. If you have completed homework 1., then try to create chord
3. Run chunks
4. Run map
