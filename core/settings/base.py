import os
from datetime import timedelta
from pathlib import Path

import dotenv

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file, override=True)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    # django default apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # my apps
    "users",
    "main",
    "management",
    "facility",
    "membership",
    "notification",
    "iot",
    "blog",
    "utility",
    # 3rd party apps
    "rest_framework",
    "rest_framework_simplejwt",
    "djoser",
    "corsheaders",
    "social_django",
    "channels",
    "django_filters",
    "django_celery_results",
    "django_celery_beat",
    "import_export",
    # dev dependency
    "django_extensions",
    # "debug_toolbar",
    "drf_spectacular",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # whitenoise middleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # cors middleware
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "debug_toolbar.middleware.DebugToolbarMiddleware",  # debug toolbar middleware 
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Dhaka"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# STORAGES = {
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTHENTICATION_BACKENDS = [
    "users.backends.EmailAndUsernameBackend",  # custom backend for email and username login
    "social_core.backends.facebook.FacebookOAuth2",
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "users.authentication.CustomJWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

AUTH_USER_MODEL = "users.User"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=3),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=10),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
}

DJOSER = {
    "LOGIN_FIELD": "email",
    "USER_CREATE_PASSWORD_RETYPE": True,
    "ACTIVATION_URL": "auth/activation/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": True,
    "SEND_CONFIRMATION_EMAIL": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    "PASSWORD_RESET_CONFIRM_URL": "auth/password-reset/{uid}/{token}",
    "SET_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND": True,
    "TOKEN_MODEL": None,
    "SERIALIZERS": {
        "user_create": "users.serializers.UserCreateSerializer",
        "user": "users.serializers.UserSerializer",
        "current_user": "users.serializers.UserSerializer",
        "user_delete": "djoser.serializers.UserDeleteSerializer",
    },
    "SOCIAL_AUTH_ALLOWED_REDIRECT_URIS": os.getenv("REDIRECT_URLS", "").split(","),
}


AUTH_COOKIE = "access"
AUTH_COOKIE_MAX_AGE = 60 * 60 * 24
AUTH_COOKIE_SECURE = os.getenv("AUTH_COOKIE_SECURE", "True") == "True"
AUTH_COOKIE_HTTP_ONLY = True
AUTH_COOKIE_PATH = "/"
AUTH_COOKIE_SAMESITE = "Lax"

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv("GOOGLE_AUTH_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv("GOOGLE_AUTH_SECRET_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]

SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ["username"]

SOCIAL_AUTH_FACEBOOK_KEY = os.getenv("FACEBOOK_AUTH_KEY")
SOCIAL_AUTH_FACEBOOK_SECRET = os.getenv("FACEBOOK_AUTH_SECRET_KEY")

SOCIAL_AUTH_FACEBOOK_SCOPE = ["email"]
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {"fields": "email, first_name, last_name"}

# MQTT SETTINGS
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")
MQTT_KEEPALIVE = int(os.getenv("MQTT_KEEPALIVE", 60))
MQTT_TLS_ENABLED = False
MQTT_TLS_CA_FILE = None


REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# CHANNELS SETTINGS

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

# CELERY SETTINGS

CELERY_TIMEZONE = "Asia/Dhaka"

CELERY_BROKER_URL = f"{REDIS_URL}/1"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "TIMEOUT": 10 * 60,
        "LOCATION": f"{REDIS_URL}/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

CELERY_BEAT_SCHEDULE = {
    "notify_customers": {
        "task": "notification.tasks.notify_customers",
        "schedule": 5,
        "args": ["Hello World"],
    }
}

####################
# Stripe Settings #
####################

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")

########################
# Spectacular Settings #
########################

SPECTACULAR_SETTINGS = {
    "TITLE": "Zenith System API",
    "DESCRIPTION": "A cutting edge API for Hotel Management System",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

#####################
# LOGGING SETTINGS #
#####################

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#         },
#         "logfile": {
#             "level": "DEBUG",
#             "class": "logging.handlers.RotatingFileHandler",
#             "filename": BASE_DIR / "logs/debug.log",
#             "maxBytes": 5000,
#             "backupCount": 2,
#             "formatter": "verbose",
#         },
#     },
#     "loggers": {
#         "": {
#             "handlers": ["console", "logfile"],
#             "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
#         },
#     },
#     "formatters": {
#         "verbose": {
#             "format": "{asctime} ({levelname}) - {name} - {message}",
#             "style": "{",
#         },
#     },
# }

# Ensure the logs directory exists
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)


###################
# Unfold Settings #
###################

UNFOLD = {
    "SITE_TITLE": "Zenith System",
    "SITE_HEADER": "Zenith System",
    "SITE_URL": "/",
}
