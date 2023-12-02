from .base import *
from dotenv import load_dotenv
import os

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG")

ALLOWED_HOSTS = []

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CSRF_TRUSTED_ORIGINS = []


DATABASES = {
    "default": dj_database_url.parse(os.environ.get("DATABASE_URL"), conn_max_age=600),
}
