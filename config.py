import os
from dotenv import load_dotenv

load_dotenv()


database_uri = os.getenv("DATABASE_URL", "sqlite:///database.db")

if database_uri.startswith("postgres://"):
    database_uri = database_uri.replace("postgres://", "postgresql://", 1)

class Config:
    SQLALCHEMY_DATABASE_URI = database_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False