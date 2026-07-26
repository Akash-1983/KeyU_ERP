from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():

    app = Flask(__name__)

    # Configuration
    app.config.from_object("config.Config")

    # Initialize Database
    db.init_app(app)

    # ==========================
    # Import Models
    # ==========================
    from app.models.customer import Customer
    from app.models.product import Product
    from app.models.user import User
    from app.models.printer import Printer

    # ==========================
    # Import Blueprints
    # ==========================
    from app.routes.auth import auth
    from app.routes.dashboard import dashboard
    from app.routes.customer import customer
    from app.routes.product import product
    from app.routes.printer import printer

    # ==========================
    # Register Blueprints
    # ==========================
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(customer)
    app.register_blueprint(product)
    app.register_blueprint(printer)

    # ==========================
    # Create Database Tables
    # ==========================
    with app.app_context():
        db.create_all()

    return app