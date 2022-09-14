from myshop.celery import app
import json
from oscar.core.loading import get_class

ProductClass = get_class("catalogue.models", "ProductClass")
Product = get_class("catalogue.models", "Product")


@app.task
def import_data(json_file):
    cloths = ProductClass.objects.get_or_create(name="cloths")

    with open(json_file) as f:
        products = json.load(f)["data"]

    for product in products:
        Product.objects.get_or_create(
            title=product["attributes"]["name"], product_class=cloths[0]
        )
