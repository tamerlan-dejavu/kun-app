from .base import *  # noqa: F401,F403

DEBUG = True
ALLOWED_HOSTS = ["*"]
SMS_BACKEND = "console"  # код входа пишется в лог

# dev-вход в браузерный API (см. config/urls.py)
LOGIN_REDIRECT_URL = "/api/v1/gatherings"
