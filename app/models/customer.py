from app import db


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)

    company_name = db.Column(db.String(150), nullable=False)

    username = db.Column(db.String(50), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    contact_person = db.Column(db.String(100))

    mobile = db.Column(db.String(20))

    email = db.Column(db.String(120))

    address = db.Column(db.Text)

    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # Customer -> Products Relationship
    products = db.relationship(
        "Product",
        backref="customer",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Customer {self.company_name}>"