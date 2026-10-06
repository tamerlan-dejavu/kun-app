from .base import *  # noqa: F401,F403

SMS_BACKEND = "dummy"
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
CELERY_TASK_ALWAYS_EAGER = True
CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# Кэш в памяти: тесты не трогают dev-Redis (счётчики rate limit, коды)
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
# django-ratelimit предупреждает, что LocMem не общий между процессами — в тестах это не важно
SILENCED_SYSTEM_CHECKS = ["django_ratelimit.E003", "django_ratelimit.W001"]
