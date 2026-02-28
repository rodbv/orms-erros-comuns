import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-dev-key"
DEBUG = True
ALLOWED_HOSTS: list[str] = []

TESTING = any("pytest" in arg for arg in sys.argv)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "api",
]

# Conditionally add Silk unless disabled
if not TESTING and not os.environ.get("SILK_DISABLED"):
    INSTALLED_APPS.insert(7, "silk")

# Conditionally add Django Debug Toolbar
if os.environ.get("DDT_ENABLED"):
    INSTALLED_APPS.append("debug_toolbar")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Conditionally add Silk middleware unless disabled
if not TESTING and not os.environ.get("SILK_DISABLED"):
    MIDDLEWARE.append("silk.middleware.SilkyMiddleware")

# Conditionally add Debug Toolbar middleware (should be near the top)
if os.environ.get("DDT_ENABLED"):
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
    # Debug Toolbar config
if os.environ.get("DDT_ENABLED"):
    INTERNAL_IPS = [
        "127.0.0.1",
        "localhost",
    ]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"
ASGI_APPLICATION = "backend.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SILKY_AUTHENTICATION = False
SILKY_AUTHORISATION = False
