"""Ограничения модели данных модерации — проверяются самой PostgreSQL."""

import pytest
from django.db import DatabaseError, IntegrityError, connection, transaction

from apps.chat.models import Message
from apps.moderation.models import Block, ModerationLog, Report
from tests.factories import GatheringFactory, MessageFactory, UserFactory

pytestmark = pytest.mark.django_db


def assert_db_rejects(fn, exc=IntegrityError):
    with pytest.raises(exc), transaction.atomic():
        fn()


def test_report_exactly_one_target():
    reporter, target = UserFactory(), UserFactory()
    Report.objects.create(reporter=reporter, target_type="user", target_user=target, reason="spam")
    # тип не совпадает с заполненной целью
    assert_db_rejects(
        lambda: Report.objects.create(
            reporter=reporter, target_type="gathering", target_user=target, reason="spam"
        )
    )
    # две цели сразу
    assert_db_rejects(
        lambda: Report.objects.create(
            reporter=reporter,
            target_type="user",
            target_user=target,
            target_gathering=GatheringFactory(),
            reason="spam",
        )
    )


def test_block_not_self_and_once():
    a, b = UserFactory(), UserFactory()
    assert_db_rejects(lambda: Block.objects.create(blocker=a, blocked=a))
    Block.objects.create(blocker=a, blocked=b)
    assert_db_rejects(lambda: Block.objects.create(blocker=a, blocked=b))


def test_system_message_requires_event():
    g = GatheringFactory()
    assert_db_rejects(lambda: Message.objects.create(gathering=g, kind="system"))
    assert_db_rejects(lambda: MessageFactory(gathering=g, system_event="joined"))


def test_moderation_log_reason_required():
    actor = UserFactory()
    assert_db_rejects(
        lambda: ModerationLog.objects.create(
            actor=actor, action="warn", target_type="user", target_id=1, reason=""
        )
    )


def test_moderation_log_immutable_in_db():
    """Триггер запрещает UPDATE/DELETE даже мимо ORM (DataGrip, psql)."""
    log = ModerationLog.objects.create(
        actor=UserFactory(), action="warn", target_type="user", target_id=1, reason="тест"
    )
    table = ModerationLog._meta.db_table

    def raw(sql):
        with connection.cursor() as cur:
            cur.execute(sql, [log.pk])

    assert_db_rejects(lambda: raw(f"UPDATE {table} SET reason = 'x' WHERE id = %s"), DatabaseError)
    assert_db_rejects(lambda: raw(f"DELETE FROM {table} WHERE id = %s"), DatabaseError)

    with pytest.raises(PermissionError):
        log.save()
    with pytest.raises(PermissionError):
        log.delete()
