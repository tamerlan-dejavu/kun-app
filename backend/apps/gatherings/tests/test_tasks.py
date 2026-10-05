"""Фоновые задачи сборов: finished, напоминания, «Как прошла встреча?», итог."""

from datetime import timedelta

import pytest
from django.utils import timezone

from apps.gatherings import tasks
from apps.gatherings.models import Attendance, Gathering
from tests.factories import GatheringFactory, ParticipationFactory

pytestmark = pytest.mark.django_db


def gathering(starts_in: timedelta, members=2, created_ago=timedelta(days=1), **kwargs):
    """Сбор с участниками; created_at и starts_at выставляем мимо проверок модели."""
    g = GatheringFactory(**kwargs)
    users = [ParticipationFactory(gathering=g).user for _ in range(members)]
    now = timezone.now()
    Gathering.objects.filter(pk=g.pk).update(
        starts_at=now + starts_in, created_at=now - created_ago
    )
    g.refresh_from_db()
    return g, users


def test_finish_started():
    started, _ = gathering(-timedelta(minutes=1))
    full, _ = gathering(-timedelta(minutes=1), status="full")
    future, _ = gathering(timedelta(hours=1))
    assert tasks.finish_gatherings() == 2
    statuses = dict(Gathering.objects.values_list("pk", "status"))
    assert statuses[started.pk] == statuses[full.pk] == "finished"
    assert statuses[future.pk] == "open"


def test_reminder_once(sent_notifications):
    g, users = gathering(timedelta(hours=1, minutes=55))
    assert tasks.send_reminders() == 1
    assert {(uid, t) for uid, t, *_ in sent_notifications} == {(u.pk, "reminder") for u in users}
    assert tasks.send_reminders() == 0  # повторный запуск ничего не шлёт
    assert len(sent_notifications) == 2


def test_reminder_skips_far_and_freshly_created(sent_notifications):
    gathering(timedelta(hours=3))  # ещё рано
    gathering(timedelta(hours=1, minutes=30), created_ago=timedelta(minutes=10))  # только создали
    assert tasks.send_reminders() == 0
    assert sent_notifications == []


def test_after_prompt(sent_notifications):
    g, users = gathering(-timedelta(hours=1, minutes=5), status="finished")
    gathering(-timedelta(minutes=30), status="finished")  # ещё рано
    gathering(-timedelta(hours=13), status="finished")  # окно отметки закрыто
    assert tasks.send_after_prompts() == 1
    assert {uid for uid, *_ in sent_notifications} == {u.pk for u in users}
    assert sent_notifications[0][1] == "after_prompt"


@pytest.mark.parametrize("came, happened", [(2, True), (1, False)])
def test_settle(came, happened):
    g, users = gathering(-timedelta(hours=13), members=3, status="finished")
    for u in users[:came]:
        Attendance.objects.create(gathering=g, user=u)
    assert tasks.settle_gatherings() == 1
    g.refresh_from_db()
    assert g.happened is happened and g.settled_at is not None
    for u in users:
        u.refresh_from_db()
    counts = [u.happened_gatherings_count for u in users]
    assert counts == ([1] * came + [0] * (3 - came) if happened else [0, 0, 0])
    assert tasks.settle_gatherings() == 0  # итог подводится один раз


def test_settle_waits_for_attendance_window():
    gathering(-timedelta(hours=11), status="finished")
    assert tasks.settle_gatherings() == 0
