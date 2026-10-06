"""Жалобы и блокировки через API."""

import pytest

from apps.moderation.models import Block, Report
from tests.factories import GatheringFactory, MessageFactory, ParticipationFactory, UserFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def alerts(monkeypatch):
    """Перехват алертов модераторам; on_commit выполняется сразу."""
    from apps.moderation import services, tasks

    sent = []
    monkeypatch.setattr(services.transaction, "on_commit", lambda fn: fn())
    monkeypatch.setattr(tasks.alert_moderators, "delay", lambda rid: sent.append(rid))
    return sent


def report(client, **body):
    return client.post("/api/v1/reports", body, format="json")


def test_critical_report_alerts_and_dedups(client_for, user, alerts):
    other = UserFactory()
    client = client_for(user)
    r = report(client, target_type="user", target_id=other.id, reason="danger", text="Угрозы")
    assert r.status_code == 201
    rep = Report.objects.get(pk=r.json()["id"])
    assert rep.priority == "critical" and rep.target_user == other
    assert alerts == [rep.pk]  # критичная — сразу модераторам
    again = report(client, target_type="user", target_id=other.id, reason="spam")
    assert again.json()["id"] == rep.pk  # открытая жалоба не дублируется


def test_normal_report_not_alerted(client_for, user, alerts):
    report(client_for(user), target_type="user", target_id=UserFactory().id, reason="spam")
    assert Report.objects.get().priority == "normal"
    assert alerts == []


def test_report_message_only_from_participant(client_for, user, alerts):
    msg = MessageFactory()
    client = client_for(user)
    assert report(client, target_type="message", target_id=msg.id, reason="spam").status_code == 404
    ParticipationFactory(gathering=msg.gathering, user=user)
    assert report(client, target_type="message", target_id=msg.id, reason="spam").status_code == 201


def test_report_self_and_missing(client_for, user, alerts):
    client = client_for(user)
    r = report(client, target_type="user", target_id=user.id, reason="spam")
    assert r.json()["code"] == "report_self"
    assert (
        report(client, target_type="gathering", target_id=999999, reason="spam").status_code == 404
    )
    hidden = GatheringFactory(moderation_status="hidden")
    r = report(client, target_type="gathering", target_id=hidden.id, reason="spam")
    assert r.status_code == 404


def test_block_and_unblock(client_for, user):
    other = UserFactory()
    client = client_for(user)
    assert client.post("/api/v1/blocks", {"user_id": other.id}, format="json").status_code == 204
    assert client.post("/api/v1/blocks", {"user_id": other.id}, format="json").status_code == 204
    assert Block.objects.filter(blocker=user, blocked=other).count() == 1
    r = client.post("/api/v1/blocks", {"user_id": user.id}, format="json")
    assert r.json()["code"] == "block_self"
    assert client.delete(f"/api/v1/blocks/{other.id}").status_code == 204
    assert not Block.objects.exists()


def test_alert_task_falls_back_to_log(caplog):
    from apps.moderation.tasks import alert_moderators

    rep = Report.objects.create(
        reporter=UserFactory(),
        target_type="user",
        target_user=UserFactory(),
        reason="danger",
        priority="critical",
    )
    with caplog.at_level("WARNING", logger="kun.moderation"):
        assert alert_moderators(rep.pk) == "log"
    assert f"#{rep.pk}" in caplog.text
