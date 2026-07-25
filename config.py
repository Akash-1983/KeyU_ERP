class Config:
    SECRET_KEY = "keyu_secret_key"

    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:akash@localhost:5432/keyu_erp"

    SQLALCHEMY_TRACK_MODIFICATIONS = False