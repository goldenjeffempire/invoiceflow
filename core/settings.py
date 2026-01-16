"""
Django settings for core project.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "unsafe-default-key")
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "accounts",
    "invoices",
    "payments",
    "dashboard",
    "sales",
    "expenses",
    "reports",
    "settings",
    "crispy_forms",
    "crispy_bootstrap5",
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'
AUTH_USER_MODEL = 'accounts.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        "OPTIONS": {"context_processors": ["django.template.context_processors.debug",
                                           "django.template.context_processors.request",
                                           "django.contrib.auth.context_processors.auth",
                                           "django.contrib.messages.context_processors.messages"]},
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

if os.getenv("RENDER"):
    import dj_database_url
    DATABASES = {
        "default": dj_database_url.config(
            default=os.getenv("DATABASE_URL"),
            conn_max_age=600,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REPLIT_DEV_DOMAIN = os.getenv("REPLIT_DEV_DOMAIN", "")
SITE_URL = os.getenv("SITE_URL", "http://localhost:5000")
if REPLIT_DEV_DOMAIN:
    SITE_URL = f"https://{REPLIT_DEV_DOMAIN}"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CSRF_TRUSTED_ORIGINS = ["https://invoiceflow.com.ng", "https://www.invoiceflow.com.ng"]
REPLIT_DEV_DOMAIN = os.getenv("REPLIT_DEV_DOMAIN", "")
if REPLIT_DEV_DOMAIN:
    CSRF_TRUSTED_ORIGINS.append(f"https://{REPLIT_DEV_DOMAIN}")

if DEBUG:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False
    X_FRAME_OPTIONS = 'SAMEORIGIN'
else:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    X_FRAME_OPTIONS = 'DENY'

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY", "")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")

LOGIN_URL = 'auth:login'
LOGIN_REDIRECT_URL = 'dashboard:home'
LOGOUT_REDIRECT_URL = 'landing'
