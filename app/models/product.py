from app import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    # Auto Generated Product Number
    product_no = db.Column(db.String(20), unique=True, nullable=False)

    # Customer / Company
    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.id"),
        nullable=False
    )

    # Product Details
    product_name = db.Column(db.String(200), nullable=False)

    cylinder_no = db.Column(db.String(100))

    artwork_file = db.Column(db.String(255))

    # Status
    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def __repr__(self):
        return f"<Product {self.product_name}>"