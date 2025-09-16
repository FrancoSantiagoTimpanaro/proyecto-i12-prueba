import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Preferir DATABASE_URL si está presente (formato SQLAlchemy)
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # fallback usando las variables de postgres de docker-compose
        user = os.environ.get("POSTGRES_USER", "i12user")
        pw   = os.environ.get("POSTGRES_PASSWORD", "i12pass")
        host = os.environ.get("POSTGRES_HOST", "postgres")
        port = os.environ.get("POSTGRES_PORT", "5432")
        db   = os.environ.get("POSTGRES_DB", "i12db")
        SQLALCHEMY_DATABASE_URI = f"postgresql://{user}:{pw}@{host}:{port}/{db}"
