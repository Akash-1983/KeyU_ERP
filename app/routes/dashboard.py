from flask import Blueprint, render_template
from app.models.customer import Customer
from app.models.product import Product

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/")
def home():

    customer_count = Customer.query.count()

    product_count = Product.query.count()

    return render_template(
        "dashboard.html",
        customer_count=customer_count,
        product_count=product_count
    )