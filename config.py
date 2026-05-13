import os

class Config:
    uri = os.getenv("DATABASE_URL", "sqlite:///database.db")

    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://postgres:jKUlMHowpUVQhwjoWmMIcSRdwqYvMWdh@switchback.proxy.rlwy.net:21944/railway")

    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
