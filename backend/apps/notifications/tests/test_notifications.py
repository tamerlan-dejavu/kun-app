"""Диспетчер уведомлений и доставка по каналам."""

from datetime import timedelta

import httpx
import pytest
from django.test import override_settings
from django.utils import timezone

from apps.accounts.sms import dummy, mask
from apps.gatherings.models import Gathering
from apps.notifications.dispatcher import gathering_context, notify
from apps.notifications.models import NotificationSettings, TelegramLink
from apps.notifications.tasks import deliver
from tests.factories import GatheringFactory, ParticipationFactory, UserFactory

pytestmark = pytest.mark.django_db
URL = "/api/v1/gatherings"


def group(members=2, **kwargs):
    g = GatheringFactory(**kwargs)
    ParticipationFactory(gathering=g, user=g.creator, is_creator=True)
    others = [ParticipationFactory(gathering=g).user for _ in range(members)]
    return g, others


# --- кому ---


def test_settings_respected_but_cancel_always_on(sent_notifications):
    a, b = UserFactory(), UserFactory()
    NotificationSettings.objects.create(user=a, reminder=False)
    ctx = gathering_context(GatheringFactory())
    notify([a.pk, b.pk], "reminder", ctx)
    notify([a.pk, b.pk], "cancelled", ctx)
    assert {(uid, t) for uid, t, *_ in sent_notifications} == {
        (b.pk, "reminder"),
        (a.pk, "cancelled"),
        (b.pk, "cancelled"),
    }


def test_join_and_leave_notify_creator(client_for, sent_notifications):
    g, _ = group(members=0)
    newcomer = UserFactory()
    client = client_for(newcomer)
    client.post(f"{URL}/{g.id}/join")
    client.post(f"{URL}/{g.id}/leave")
    assert [(uid, t, ctx["joined"]) for uid, t, ctx, _ in sent_notifications] == [
        (g.creator_id, "joined_left", True),
        (g.creator_id, "joined_left", False),
    ]


def test_update_notifies_others(client_for, sent_notifications):
    g, others = group()
    client_for(g.creator).patch(f"{URL}/{g.id}", {"comment": "Берите зонты"}, format="json")
    assert {uid for uid, t, *_ in sent_notifications if t == "updated"} == {u.pk for u in others}


@pytest.mark.parametrize("starts_in, sms", [(timedelta(hours=2), True), (timedelta(days=1), False)])
def test_cancel_sms_only_when_urgent(client_for, sent_notifications, starts_in, sms):
    g, others = group()
    Gathering.objects.filter(pk=g.pk).update(starts_at=timezone.now() + starts_in)
    client_for(g.creator).post(f"{URL}/{g.id}/cancel", {"reason": "Заболел"}, format="json")
    cancelled = [n for n in sent_notifications if n[1] == "cancelled"]
    assert {uid for uid, *_ in cancelled} == {u.pk for u in others}
    assert all(n[3] is sms for n in cancelled)
    assert cancelled[0][2]["reason"] == "Заболел"


def test_chat_notifications_throttled(client_for, sent_notifications):
    g, (a, b) = group()
    client = client_for(a)
    for text in ("раз", "два", "три"):
        client.post(f"{URL}/{g.id}/messages", {"text": text}, format="json")
    chat = [uid for uid, t, *_ in sent_notifications if t == "chat_message"]
    # Каждый из остальных (создатель и b) — по одному разу, автор — никогда
    assert sorted(chat) == sorted([g.creator_id, b.pk])


# --- куда ---


def test_deliver_falls_back_to_log(caplog):
    user = UserFactory()
    ctx = gathering_context(GatheringFactory())
    with caplog.at_level("INFO", logger="kun.notifications"):
        assert deliver(user.pk, "reminder", ctx) == ["log"]
    assert "Через 2 часа" in caplog.text
    assert user.phone not in caplog.text


@override_settings(TELEGRAM_BOT_TOKEN="test-token")
def test_deliver_telegram(monkeypatch):
    user = UserFactory()
    TelegramLink.objects.create(user=user, chat_id=42, linked_at=timezone.now())
    posted = []

    def fake_post(url, json, timeout):
        posted.append(json)
        return httpx.Response(200, request=httpx.Request("POST", url))

    monkeypatch.setattr(httpx, "post", fake_post)
    g = GatheringFactory()
    assert deliver(user.pk, "reminder", gathering_context(g)) == ["telegram"]
    assert posted[0]["chat_id"] == 42
    assert g.slug in posted[0]["reply_markup"]["inline_keyboard"][0][0]["url"]


def test_deliver_sms_masks_phone_in_logs():
    dummy.outbox.clear()
    user = UserFactory()
    ctx = gathering_context(GatheringFactory(), reason="Дождь")
    assert "sms" in deliver(user.pk, "cancelled", ctx, sms=True)
    assert dummy.outbox == [(user.phone, f"Сбор «{ctx['title']}» отменён: Дождь")]
    assert mask("+77011234567") == "+7701*****67"
