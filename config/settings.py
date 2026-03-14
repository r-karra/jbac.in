import os
import sys
from pathlib import Path

try:
    import dj_database_url
except ImportError:
    dj_database_url = None

BASE_DIR = Path(__file__).resolve().parent.parent

default_allowed_hosts = [
    "127.0.0.1",
    "localhost",
    "rkarra.pythonanywhere.com",
]

SECRET_KEY = os.getenv("SECRET_KEY", "jbac-development-secret-key")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = [host.strip() for host in os.getenv("ALLOWED_HOSTS", ",".join(default_allowed_hosts)).split(",") if host.strip()]
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if origin.strip()]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "core",
    "accounts",
    "directory",
    "updates",
    "api",
    "meetings",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"

default_sqlite_db = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": BASE_DIR / "db.sqlite3",
}

if dj_database_url is not None:
    DATABASES = {
        "default": dj_database_url.config(
            default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
            conn_max_age=600,
        )
    }
else:
    DATABASES = {"default": default_sqlite_db}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


LANGUAGE_CODE = "en-in"

LANGUAGES = [
    ("en", "English"),
    ("te", "Telugu"),
]

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

if "test" in sys.argv:
    STORAGES["staticfiles"] = {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    }

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

AUTH_USER_MODEL = "accounts.User"
AUTHENTICATION_BACKENDS = [
    "config.auth_backends.EmailOrMobileBackend",
    "django.contrib.auth.backends.ModelBackend",
]

LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "core:dashboard"
LOGOUT_REDIRECT_URL = "core:home"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

OTP_PROVIDER = os.getenv("OTP_PROVIDER", "console").lower()
OTP_TWILIO_ACCOUNT_SID = os.getenv("OTP_TWILIO_ACCOUNT_SID", "")
OTP_TWILIO_AUTH_TOKEN = os.getenv("OTP_TWILIO_AUTH_TOKEN", "")
OTP_TWILIO_FROM_NUMBER = os.getenv("OTP_TWILIO_FROM_NUMBER", "")
OTP_MSG91_AUTH_KEY = os.getenv("OTP_MSG91_AUTH_KEY", "")
OTP_MSG91_SENDER_ID = os.getenv("OTP_MSG91_SENDER_ID", "JBACOT")
OTP_MSG91_TEMPLATE_ID = os.getenv("OTP_MSG91_TEMPLATE_ID", "")
OTP_MAX_VERIFY_ATTEMPTS = int(os.getenv("OTP_MAX_VERIFY_ATTEMPTS", "5"))
OTP_LOCK_MINUTES = int(os.getenv("OTP_LOCK_MINUTES", "15"))
OTP_MAX_REQUESTS_PER_WINDOW = int(os.getenv("OTP_MAX_REQUESTS_PER_WINDOW", "5"))
OTP_REQUEST_WINDOW_MINUTES = int(os.getenv("OTP_REQUEST_WINDOW_MINUTES", "15"))

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
