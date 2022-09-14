### More realistic celery + django integration (django-oscar)

Django-oscar is platform for creating e-commerce shop. This platform is build with Django.
I have created simple e-shop called myshop. I have followed steps from official
documentation https://django-oscar.readthedocs.io/en/stable/internals/getting_started.html
and I have forked catalogue app, where I will put our task. Task in which we will import
sample products. I have downloaded sample products from page
https://demo.spreecommerce.org/api/v2/storefront/products .

### Code
To obey convention, we have celery in 3 places:
1. `myshop/settings.py` - configuration of celery
2. `myshop/celery.py` - celery app object
3. `catalogue/tasks.py` - tasks are located in app's `tasks.py` files

Example code of task is in `catalogue/tasks.py`

### Run
Download one page of products from https://demo.spreecommerce.org/api/v2/storefront/products .
Save it in folder `catalogue/external_fixtures/products_page1.json`. Start docker compose
`docker-compose up --build`. In second shell session start django:
`docker-compose exec django bash`. Inside it call `./manage.py shell`. Then inside django
shell run:
```python
from catalogue.tasks import import_data
res = import_data.delay("/app/catalogue/external_fixtures/products_page1.json")
```

### FAQ
**Q: Can I use celery task to generate PDF report?**

A: Yes.

**Q: Can I use celery task send a email newsletter?**

A: Yes.

### Homework
1. Create solr service in docker-compose, and configure haystack connection to it.
2. Create task to fetch json pages, instead of doing manually.
