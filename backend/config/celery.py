import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

app = Celery("kun")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Все задачи идемпотентны — пропущенный или двойной запуск не ломает данные
EVERY_5_MIN = crontab(minute="*/5")

app.conf.beat_schedule = {
    "gatherings-finish-started": {
        "task": "apps.gatherings.tasks.finish_gatherings",
        "schedule": EVERY_5_MIN,
    },
    "gatherings-send-reminders": {
        "task": "apps.gatherings.tasks.send_reminders",
        "schedule": EVERY_5_MIN,
    },
    "gatherings-send-after-prompts": {
        "task": "apps.gatherings.tasks.send_after_prompts",
        "schedule": EVERY_5_MIN,
    },
    "gatherings-settle": {
        "task": "apps.gatherings.tasks.settle_gatherings",
        "schedule": EVERY_5_MIN,
    },
}
