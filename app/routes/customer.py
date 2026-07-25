from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.customer import Customer

customer = Blueprint("customer", __name__)


# ==========================
# Customer List
# ==========================
@customer.route("/customers")
def customer_list():

    customers = Customer.query.order_by(Customer.company_name).all()

    return render_template(
        "customers.html",
        customers=customers
    )


# ==========================
# Add Customer
# ==========================
@customer.route("/customers/add", methods=["GET", "POST"])
def add_customer():

    if request.method == "POST":

        customer = Customer(

            company_name=request.form["company_name"],

            username=request.form["username"],

            password=request.form["password"],

            contact_person=request.form["contact_person"],

            mobile=request.form["mobile"],

            email=request.form["email"],

            address=request.form["address"]

        )

        db.session.add(customer)

        db.session.commit()

        flash("Customer Added Successfully")

        return redirect(url_for("customer.customer_list"))

    return render_template("customer_form.html")


# ==========================
# Edit Customer
# ==========================
@customer.route("/customers/edit/<int:id>", methods=["GET", "POST"])
def edit_customer(id):

    customer = Customer.query.get_or_404(id)

    if request.method == "POST":

        customer.company_name = request.form["company_name"]

        customer.username = request.form["username"]

        customer.password = request.form["password"]

        customer.contact_person = request.form["contact_person"]

        customer.mobile = request.form["mobile"]

        customer.email = request.form["email"]

        customer.address = request.form["address"]

        db.session.commit()

        flash("Customer Updated Successfully")

        return redirect(url_for("customer.customer_list"))

    return render_template(
        "customer_form.html",
        customer=customer
    )


# ==========================
# Delete Customer
# ==========================
@customer.route("/customers/delete/<int:id>")
def delete_customer(id):

    customer = Customer.query.get_or_404(id)

    db.session.delete(customer)

    db.session.commit()

    flash("Customer Deleted Successfully")

    return redirect(url_for("customer.customer_list"))