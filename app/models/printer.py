from app import db

class Printer(db.Model):
    __tablename__ = "printers"

    id = db.Column(db.Integer, primary_key=True)

    printer_no = db.Column(db.String(20), unique=True, nullable=False)

    printer_name = db.Column(db.String(150), nullable=False)

    contact_person = db.Column(db.String(100))

    mobile = db.Column(db.String(20))

    email = db.Column(db.String(100))

    gst_no = db.Column(db.String(30))

    address = db.Column(db.Text)

    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def __repr__(self):
        return f"<Printer {self.printer_name}>"