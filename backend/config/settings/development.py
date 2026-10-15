"""
Development settings for Darsentra ERP.
Includes developer-friendly configurations, debugging aids, and flexible database options.
"""
import os

from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,backend,[::1]"
    ).split(",")
    if host.strip()
]

# Database configuration
# When running in Docker, DB_HOST='db' and DB_ENGINE='django.db.backends.postgresql'.
# When running locally without Docker or PostgreSQL service, defaults smoothly to SQLite.
db_engine = os.getenv("DB_ENGINE", "")
db_host = os.getenv("DB_HOST", "")

if db_engine == "django.db.backends.postgresql" or db_host:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME", "darsentra_erp"),
            "USER": os.getenv("DB_USER", "darsentra_user"),
            "PASSWORD": os.getenv("DB_PASSWORD", "darsentra_dev_password"),
            "HOST": db_host or "localhost",
            "PORT": os.getenv("DB_PORT", "5432"),
            "CONN_MAX_AGE": 0,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# DRF configuration in development: add Browsable API
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",
]

# Email Backend for development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
