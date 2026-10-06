from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR.parent / ".env")

SECRET_KEY = env("SECRET_KEY")
DEBUG = False
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
SITE_URL = env("SITE_URL", default="http://localhost")

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    # third-party
    "rest_framework",
    "django_filters",
    "drf_spectacular",
    "channels",
    "django_celery_beat",
    # KUN
    "apps.common",
    "apps.accounts",
    "apps.universities",
    "apps.catalog",
    "apps.gatherings",
    "apps.chat",
    "apps.notifications",
    "apps.moderation",
    "apps.places",
    "apps.analytics",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.accounts.middleware.BlockedUserMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ENGINE"] = "django.contrib.gis.db.backends.postgis"

REDIS_URL = env("REDIS_URL", default="redis://localhost:6379/0")
CACHES = {
    "default": {"BACKEND": "django.core.cache.backends.redis.RedisCache", "LOCATION": REDIS_URL}
}

AUTH_USER_MODEL = "accounts.User"
AUTHENTICATION_BACKENDS = ["apps.accounts.backends.PhoneBackend"]

# Сессии в httpOnly-куки (веб)
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30

# Язык и время: интерфейс на русском, даты в UTC, показ в Asia/Almaty
LANGUAGE_CODE = "ru"
LANGUAGES = [("ru", "Русский")]  # этап 2: ("kk", "Қазақша")
LOCALE_PATHS = [BASE_DIR / "locale"]
TIME_ZONE = "UTC"
DISPLAY_TIME_ZONE = "Asia/Almaty"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework.authentication.SessionAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["apps.common.permissions.IsActiveUser"],
    "DEFAULT_PAGINATION_CLASS": "apps.common.pagination.DefaultCursorPagination",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "apps.common.exceptions.exception_handler",
    "PAGE_SIZE": 20,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "KUN API",
    "VERSION": "1.0.0",
    "SCHEMA_PATH_PREFIX": "/api/v1",
    "COMPONENT_SPLIT_REQUEST": True,
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [REDIS_URL]},
    }
}

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_TIMEZONE = "UTC"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# Хранилище фото: S3-совместимое у казахстанского провайдера
S3_BUCKET = env("S3_BUCKET", default="")
if S3_BUCKET:
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                "bucket_name": S3_BUCKET,
                "endpoint_url": env("S3_ENDPOINT_URL"),
                "access_key": env("S3_ACCESS_KEY"),
                "secret_key": env("S3_SECRET_KEY"),
            },
        },
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }

EMAIL_CONFIG = env.email_url("EMAIL_URL", default="consolemail://")
vars().update(EMAIL_CONFIG)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="noreply@kun.kz")

# Внешние сервисы
SMS_BACKEND = env("SMS_BACKEND", default="console")
SMS_API_KEY = env("SMS_API_KEY", default="")
SMS_SENDER = env("SMS_SENDER", default="KUN")
DGIS_API_KEY = env("DGIS_API_KEY", default="")
TELEGRAM_BOT_TOKEN = env("TELEGRAM_BOT_TOKEN", default="")
TELEGRAM_BOT_USERNAME = env("TELEGRAM_BOT_USERNAME", default="")
TELEGRAM_WEBHOOK_SECRET = env("TELEGRAM_WEBHOOK_SECRET", default="")
TELEGRAM_MODERATORS_CHAT_ID = env("TELEGRAM_MODERATORS_CHAT_ID", default="")
VAPID_PUBLIC_KEY = env("VAPID_PUBLIC_KEY", default="")
VAPID_PRIVATE_KEY = env("VAPID_PRIVATE_KEY", default="")
VAPID_SUBJECT = env("VAPID_SUBJECT", default="mailto:support@kun.kz")
POSTHOG_API_KEY = env("POSTHOG_API_KEY", default="")
POSTHOG_HOST = env("POSTHOG_HOST", default="")
SENTRY_DSN = env("SENTRY_DSN", default="")

# Бизнес-правила (раздел 3 ТЗ)
KUN = {
    "AUTH_CODE_TTL_SECONDS": 5 * 60,
    "AUTH_CODE_LENGTH": 6,
    "AUTH_MAX_ATTEMPTS": 5,
    "AUTH_LOCK_SECONDS": 15 * 60,
    "PHOTO_MAX_BYTES": 5 * 1024 * 1024,
    "INTERESTS_MIN": 3,
    "INTERESTS_MAX": 5,
    "GATHERING_TITLE_MAX": 60,
    "GATHERING_COMMENT_MAX": 300,
    "GATHERING_MIN_LEAD_HOURS": 1,
    "GATHERING_MAX_LEAD_DAYS": 14,
    "GATHERING_SEATS_MIN": 3,
    "GATHERING_SEATS_MAX": 6,
    "GATHERING_ACTIVE_PER_CREATOR": 3,
    "LATE_CANCEL_HOURS": 2,
    "SMS_CANCEL_THRESHOLD_HOURS": 3,
    "REMINDER_BEFORE_HOURS": 2,
    "AFTER_PROMPT_HOURS": 1,
    "ATTENDANCE_WINDOW_HOURS": 12,
    "RATING_WINDOW_HOURS": 48,  # в ТЗ не задано — допущение, уточнить
    "CHAT_MESSAGE_MAX": 1000,
    "CHAT_READONLY_AFTER_HOURS": 24,
    "CHAT_NOTIFY_THROTTLE_MINUTES": 10,
    "RELIABILITY_WINDOW": 10,
    "SANCTION_PAUSE_DAYS": 7,
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"pii": {"()": "apps.common.logging.PiiFilter"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "filters": ["pii"]}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
