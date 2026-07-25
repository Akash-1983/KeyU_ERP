from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app import db
from app.models.product import Product
from app.models.customer import Customer
import os

product = Blueprint("product", __name__)

UPLOAD_FOLDER = "app/static/artwork"


# ==========================================
# AUTO PRODUCT NUMBER
# ==========================================
def generate_product_no():

    last_product = Product.query.order_by(Product.id.desc()).first()

    if last_product:

        last_no = int(last_product.product_no.replace("P", ""))

        new_no = last_no + 1

    else:

        new_no = 1

    return f"P{new_no:06d}"


# ==========================================
# TEST
# ==========================================
@product.route("/test")
def test():

    return "Product Blueprint Working"


# ==========================================
# PRODUCT LIST
# ==========================================
@product.route("/products")
def products():

    search = request.args.get("search", "")

    if search:

        products = Product.query.join(Customer).filter(

            (Product.product_name.ilike(f"%{search}%")) |

            (Customer.company_name.ilike(f"%{search}%"))

        ).all()

    else:

        products = Product.query.order_by(Product.id.desc()).all()

    return render_template(

        "products.html",

        products=products,

        search=search

    )

# ==========================================
# ADD PRODUCT
# ==========================================
@product.route("/products/add", methods=["GET", "POST"])
def add_product():

    customers = Customer.query.order_by(Customer.company_name).all()

    if request.method == "POST":

        print("POST Request Received")
        
        customer_id = request.form["customer"]

        product_name = request.form["product_name"].strip()

        cylinder_no = request.form["cylinder_no"].strip()

        # Duplicate Product Check
        duplicate = Product.query.filter_by(
            customer_id=customer_id,
            product_name=product_name
        ).first()

        if duplicate:

            flash(
                "This Product already exists for this Company.",
                "danger"
            )

            return render_template(
                "product_form.html",
                customers=customers,
                product_no=generate_product_no()
            )

        artwork = request.files.get("artwork")

        filename = ""

        if artwork and artwork.filename != "":

            print("UPLOAD_FOLDER =", UPLOAD_FOLDER)
            print("ABS PATH =", os.path.abspath(UPLOAD_FOLDER))
            print("IS DIR =", os.path.isdir(UPLOAD_FOLDER))

            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            filename = secure_filename(artwork.filename)

            artwork.save(
                os.path.join(
                    UPLOAD_FOLDER,
                    filename
                )
            )

        new_product = Product(

            product_no=generate_product_no(),

            customer_id=customer_id,

            product_name=product_name,

            cylinder_no=cylinder_no,

            artwork_file=filename,

            is_active=True

        )

        db.session.add(new_product)

        db.session.commit()

        flash(
            "Product Added Successfully",
            "success"
        )

        return redirect(
            url_for("product.products")
        )

    return render_template(
        "product_form.html",
        customers=customers,
        product_no=generate_product_no()
    )


# ==========================================
# EDIT PRODUCT
# ==========================================
@product.route("/products/edit/<int:id>", methods=["GET", "POST"])
def edit_product(id):

    product_data = Product.query.get_or_404(id)

    customers = Customer.query.order_by(Customer.company_name).all()

    if request.method == "POST":

        product_data.customer_id = request.form["customer"]

        product_data.product_name = request.form["product_name"]

        product_data.cylinder_no = request.form["cylinder_no"]

        artwork = request.files.get("artwork")

        if artwork and artwork.filename != "":

            filename = secure_filename(artwork.filename)

            print("UPLOAD_FOLDER =", UPLOAD_FOLDER)
            print("ABS PATH =", os.path.abspath(UPLOAD_FOLDER))
            print("IS DIR =", os.path.isdir(UPLOAD_FOLDER))

            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            artwork.save(
                os.path.join(
                    UPLOAD_FOLDER,
                    filename
                )
            )

            product_data.artwork_file = filename

        db.session.commit()

        flash(
            "Product Updated Successfully",
            "success"
        )

        return redirect(
            url_for("product.products")
        )

    return render_template(
        "product_form.html",
        product=product_data,
        customers=customers
    )


# ==========================================
# DELETE PRODUCT
# ==========================================
@product.route("/products/delete/<int:id>")
def delete_product(id):

    product_data = Product.query.get_or_404(id)

    db.session.delete(product_data)

    db.session.commit()

    flash(
        "Product Deleted Successfully",
        "success"
    )

    return redirect(
        url_for("product.products")
    )