from flask import Blueprint, render_template, request
from app.models.printer import Printer

printer = Blueprint("printer", __name__)

# ==========================================
# AUTO PRINTER NUMBER
# ==========================================
def generate_printer_no():

    last = Printer.query.order_by(Printer.id.desc()).first()

    if last:
        last_no = int(last.printer_no.replace("PR", ""))
        new_no = last_no + 1
    else:
        new_no = 1

    return f"PR{new_no:06d}"


# ==========================================
# PRINTER LIST
# ==========================================
@printer.route("/printers")
def printers():

    search = request.args.get("search", "").strip()

    query = Printer.query

    if search:

        query = query.filter(
            Printer.printer_name.ilike(f"%{search}%")
        )

    printers = query.order_by(
        Printer.id.desc()
    ).all()

    return render_template(
        "printers.html",
        printers=printers,
        search=search
    )
from flask import redirect, url_for, flash
from app import db

# ==========================================
# ADD PRINTER
# ==========================================
@printer.route("/printers/add", methods=["GET", "POST"])
def add_printer():

    if request.method == "POST":

        printer_name = request.form["printer_name"].strip()
        contact_person = request.form["contact_person"].strip()
        mobile = request.form["mobile"].strip()
        email = request.form["email"].strip()
        gst_no = request.form["gst_no"].strip()
        address = request.form["address"].strip()

        # Duplicate Check
        duplicate = Printer.query.filter_by(
            printer_name=printer_name
        ).first()

        if duplicate:

            flash(
                "Printer already exists.",
                "danger"
            )

            return render_template(
                "printer_form.html",
                printer_no=generate_printer_no()
            )

        new_printer = Printer(

            printer_no=generate_printer_no(),

            printer_name=printer_name,

            contact_person=contact_person,

            mobile=mobile,

            email=email,

            gst_no=gst_no,

            address=address,

            is_active=True

        )

        db.session.add(new_printer)

        db.session.commit()

        flash(
            "Printer Added Successfully",
            "success"
        )

        return redirect(
            url_for("printer.printers")
        )

    return render_template(
        "printer_form.html",
        printer_no=generate_printer_no()
    )
# ==========================================
# EDIT PRINTER
# ==========================================
@printer.route("/printers/edit/<int:id>", methods=["GET", "POST"])
def edit_printer(id):

    printer_data = Printer.query.get_or_404(id)

    if request.method == "POST":

        printer_data.printer_name = request.form["printer_name"].strip()
        printer_data.contact_person = request.form["contact_person"].strip()
        printer_data.mobile = request.form["mobile"].strip()
        printer_data.email = request.form["email"].strip()
        printer_data.gst_no = request.form["gst_no"].strip()
        printer_data.address = request.form["address"].strip()

        db.session.commit()

        flash(
            "Printer Updated Successfully",
            "success"
        )

        return redirect(
            url_for("printer.printers")
        )

    return render_template(
        "printer_form.html",
        printer=printer_data
    )
# ==========================================
# DELETE PRINTER
# ==========================================
@printer.route("/printers/delete/<int:id>")
def delete_printer(id):

    printer_data = Printer.query.get_or_404(id)

    db.session.delete(printer_data)

    db.session.commit()

    flash(
        "Printer Deleted Successfully",
        "success"
    )

    return redirect(
        url_for("printer.printers")
    )