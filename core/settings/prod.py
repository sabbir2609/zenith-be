import os
from .base import *
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = (
    [os.environ["WEBSITE_HOSTNAME"]] if "WEBSITE_HOSTNAME" in os.environ else []
)

CSRF_TRUSTED_ORIGINS = (
    ["https://" + os.environ["WEBSITE_HOSTNAME"]]
    if "WEBSITE_HOSTNAME" in os.environ
    else []
)

DEBUG = False

DATABASES = {
    "default": dj_database_url.parse(os.environ.get("DATABASE_URL"), conn_max_age=600),
}
