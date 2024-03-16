import os
from .base import *  # noqa: F403

import dj_database_url  # noqa: F401

import dotenv

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file, override=True)


SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG")

ALLOWED_HOSTS = os.getenv(
    "WEBSITE_HOSTNAME",
    "127.0.0.1,localhost,192.168.133.120,*",
).split(",")

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CSRF_TRUSTED_ORIGINS = ["https://84f1-114-130-188-239.ngrok-free.app"]

CORS_ALLOW_CREDENTIALS = True

INTERNAL_IPS = [
    "127.0.0.1",
]


SITE_NAME = "Zenith System"
DOMAIN = os.environ["DOMAIN"]

# Postgres database settings

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
        "CONN_MAX_AGE": 600,
    }
}

# DATABASES = {
#     "default": dj_database_url.parse(os.environ.get("DATABASE_URL"), conn_max_age=600),
# }


# Sqlite database settings
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": "zenith",
#     }
# }


# Email configurations
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = "noreply@zenith.com"
