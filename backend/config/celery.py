import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

app = Celery("kun")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "gatherings-send-reminders": {
        "task": "apps.gatherings.tasks.send_reminders",
        "schedule": crontab(minute="*/5"),
    },
    "gatherings-finish-started": {
        "task": "apps.gatherings.tasks.finish_gatherings",
        "schedule": crontab(minute="*/5"),
    },
    "gatherings-send-after-prompts": {
        "task": "apps.gatherings.tasks.send_after_prompts",
        "schedule": crontab(minute="*/5"),
    },
    "moderation-lift-expired-pauses": {
        "task": "apps.moderation.tasks.lift_expired_pauses",
        "schedule": crontab(minute=0),
    },
    "accounts-expire-student-badges": {
        "task": "apps.universities.tasks.expire_student_badges",
        "schedule": crontab(hour=3, minute=0),
    },
}
