from flask import Blueprint, render_template, request, redirect, url_for

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Temporary Login
        if username == "admin" and password == "123456":
            return redirect(url_for("auth.dashboard"))

        return render_template(
            "login.html",
            error="Invalid Username or Password"
        )

    return render_template("login.html")


@auth.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@auth.route("/logout")
def logout():
    return redirect(url_for("auth.login"))