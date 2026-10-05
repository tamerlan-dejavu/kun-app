"""Фоновые задачи сборов (Celery Beat, раз в 5 минут — см. config/celery.py).

Каждая задача идемпотентна: отметка *_sent_at / settled_at ставится в той же транзакции,
поэтому повторный или параллельный запуск не шлёт уведомления дважды.
"""

from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.db import transaction
from django.db.models import F
from django.utils import timezone

from apps.accounts.models import User
from apps.notifications.dispatcher import gathering_context, notify
from apps.notifications.types import NotificationType

from .models import Attendance, Gathering

RULES = settings.KUN
ACTIVE = (Gathering.Status.OPEN, Gathering.Status.FULL)


def _member_ids(gathering) -> list[int]:
    return list(
        gathering.participations.filter(left_at__isnull=True).values_list("user_id", flat=True)
    )


def _claim(qs, field: str) -> list[Gathering]:
    """Забрать сборы под задачу: блокируем строки, пропуская занятые другим воркером."""
    claimed = list(qs.select_for_update(skip_locked=True))
    Gathering.objects.filter(pk__in=[g.pk for g in claimed]).update(**{field: timezone.now()})
    return claimed


@shared_task
def send_reminders() -> int:
    """Напоминание всем участникам за 2 часа до начала.
    Сборы, созданные позже чем за 2 часа до начала, не напоминаем — их только что создали."""
    now = timezone.now()
    lead = timedelta(hours=RULES["REMINDER_BEFORE_HOURS"])
    with transaction.atomic():
        due = Gathering.objects.filter(
            status__in=ACTIVE,
            moderation_status=Gathering.ModerationStatus.PUBLISHED,
            reminder_sent_at__isnull=True,
            starts_at__gt=now,
            starts_at__lte=now + lead,
            created_at__lte=F("starts_at") - lead,
        )
        gatherings = _claim(due, "reminder_sent_at")
        for g in gatherings:
            notify(_member_ids(g), NotificationType.REMINDER, gathering_context(g))
    return len(gatherings)


@shared_task
def finish_gatherings() -> int:
    """Начавшиеся сборы -> finished: пропадают из ленты, к ним больше не присоединиться."""
    return Gathering.objects.filter(status__in=ACTIVE, starts_at__lte=timezone.now()).update(
        status=Gathering.Status.FINISHED, updated_at=timezone.now()
    )


@shared_task
def send_after_prompts() -> int:
    """«Как прошла встреча?» через 1 час после начала (пока открыто окно отметки)."""
    now = timezone.now()
    with transaction.atomic():
        due = Gathering.objects.filter(
            status=Gathering.Status.FINISHED,
            moderation_status=Gathering.ModerationStatus.PUBLISHED,
            after_prompt_sent_at__isnull=True,
            starts_at__lte=now - timedelta(hours=RULES["AFTER_PROMPT_HOURS"]),
            starts_at__gt=now - timedelta(hours=RULES["ATTENDANCE_WINDOW_HOURS"]),
        )
        gatherings = _claim(due, "after_prompt_sent_at")
        for g in gatherings:
            notify(_member_ids(g), NotificationType.AFTER_PROMPT, gathering_context(g))
    return len(gatherings)


@shared_task
def settle_gatherings() -> int:
    """Итог после закрытия окна «Я пришёл» (+12 ч): сбор состоялся, если отметились >= 2.
    Тем, кто пришёл на состоявшийся сбор, +1 к счётчику в профиле.
    TODO: пересчёт надёжности, когда утвердят формулу (docs/adr/0001)."""
    now = timezone.now()
    window = timedelta(hours=RULES["ATTENDANCE_WINDOW_HOURS"])
    with transaction.atomic():
        due = Gathering.objects.filter(
            status=Gathering.Status.FINISHED, settled_at__isnull=True, starts_at__lte=now - window
        )
        # Без annotate(Count): PostgreSQL не разрешает FOR UPDATE вместе с GROUP BY
        gatherings = list(due.select_for_update(skip_locked=True))
        for g in gatherings:
            g.happened = Attendance.objects.filter(gathering=g).count() >= 2
            g.settled_at = now
            g.save(update_fields=["happened", "settled_at", "updated_at"])
            if g.happened:
                attendees = Attendance.objects.filter(gathering=g).values("user_id")
                User.objects.filter(pk__in=attendees).update(
                    happened_gatherings_count=F("happened_gatherings_count") + 1
                )
    return len(gatherings)
