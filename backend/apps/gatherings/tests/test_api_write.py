"""Создание, изменение, отмена, присоединение, выход."""

from datetime import timedelta

import pytest
from django.utils import timezone

from apps.chat.models import Message
from apps.gatherings.models import Gathering, Participation
from apps.moderation.models import BannedWord, Block, UserSanction
from tests.factories import CategoryFactory, GatheringFactory, ParticipationFactory, UserFactory

pytestmark = pytest.mark.django_db
URL = "/api/v1/gatherings"


def payload(**overrides):
    CategoryFactory(slug="walk", name="Прогулка")
    data = {
        "category": "walk",
        "title": "Прогулка по Арбату",
        "comment": "",
        "place_name": "Арбат",
        "address": "ул. Жибек Жолы",
        "district": "Алмалинский",
        "place_external_id": "2gis-123",
        "lat": 43.2617,
        "lng": 76.945,
        "starts_at": (timezone.now() + timedelta(days=1)).isoformat(),
        "seats": 4,
    }
    data.update(overrides)
    return data


def make_gathering(seats=4, members=0, **kwargs):
    """Сбор с создателем-участником и members дополнительными участниками."""
    g = GatheringFactory(seats=seats, **kwargs)
    ParticipationFactory(gathering=g, user=g.creator, is_creator=True)
    for _ in range(members):
        ParticipationFactory(gathering=g)
    return g


# --- создание ---


def test_create(client_for, user):
    r = client_for(user).post(URL, payload(), format="json")
    assert r.status_code == 201, r.json()
    data = r.json()
    assert data["is_creator"] and data["is_participant"]
    assert data["participants_count"] == 1
    assert data["moderation_status"] == "published"
    assert (data["lat"], data["lng"]) == (43.2617, 76.945)


@pytest.mark.parametrize(
    "starts_in, code",
    [(timedelta(minutes=30), "starts_too_soon"), (timedelta(days=15), "starts_too_late")],
)
def test_create_time_window(client_for, user, starts_in, code):
    starts_at = (timezone.now() + starts_in).isoformat()
    r = client_for(user).post(URL, payload(starts_at=starts_at), format="json")
    assert r.status_code == 400
    assert r.json()["code"] == code


@pytest.mark.parametrize(
    "field, value", [("seats", 7), ("title", "x" * 61), ("place_external_id", "")]
)
def test_create_validation(client_for, user, field, value):
    r = client_for(user).post(URL, payload(**{field: value}), format="json")
    assert r.status_code == 400
    assert r.json()["code"] == "validation_error"
    assert field in r.json()["fields"]


def test_create_limit_3_active(client_for, user):
    for _ in range(3):
        GatheringFactory(creator=user)
    r = client_for(user).post(URL, payload(), format="json")
    assert r.json()["code"] == "too_many_active"


def test_banned_words_go_to_pending(client_for, user):
    BannedWord.objects.create(word="казино")
    # латинская «a» вместо кириллической — тоже ловим
    r = client_for(user).post(URL, payload(comment="Потом в кaзино"), format="json")
    assert r.json()["moderation_status"] == "pending"


def test_paused_user_cannot_create(client_for, user):
    UserSanction.objects.create(
        user=user,
        kind="pause",
        reason="x",
        ends_at=timezone.now() + timedelta(days=7),
        created_by=UserFactory(),
    )
    r = client_for(user).post(URL, payload(), format="json")
    assert r.status_code == 403
    assert r.json()["code"] == "account_paused"


# --- изменение и отмена ---


def test_update_by_creator_posts_system_message(client_for):
    g = make_gathering()
    new_time = timezone.now() + timedelta(days=2)
    r = client_for(g.creator).patch(
        f"{URL}/{g.id}", {"starts_at": new_time.isoformat(), "comment": "Новое"}, format="json"
    )
    assert r.status_code == 200, r.json()
    msg = Message.objects.get(gathering=g, system_event="updated")
    assert set(msg.payload["fields"]) == {"starts_at", "comment"}


def test_update_place_must_be_complete(client_for):
    g = make_gathering()
    r = client_for(g.creator).patch(f"{URL}/{g.id}", {"place_name": "Другое"}, format="json")
    assert r.json()["code"] == "validation_error"


def test_only_creator_can_update_and_cancel(client_for, user):
    g = make_gathering()
    client = client_for(user)
    assert (
        client.patch(f"{URL}/{g.id}", {"comment": "x"}, format="json").json()["code"]
        == "not_creator"
    )
    assert client.post(f"{URL}/{g.id}/cancel", {"reason": "x"}, format="json").status_code == 403


def test_cancel(client_for):
    g = make_gathering()
    r = client_for(g.creator).post(f"{URL}/{g.id}/cancel", {"reason": "Дождь"}, format="json")
    assert r.json()["status"] == "cancelled"
    assert r.json()["cancel_reason"] == "Дождь"


# --- присоединение ---


def test_join_last_seat_makes_full(client_for, user):
    g = make_gathering(seats=3, members=1)
    r = client_for(user).post(f"{URL}/{g.id}/join")
    assert r.status_code == 200
    assert r.json()["status"] == "full"
    assert r.json()["participants_count"] == 3
    assert client_for(UserFactory()).post(f"{URL}/{g.id}/join").json()["code"] == "gathering_full"


def test_join_twice(client_for, user):
    g = make_gathering()
    client = client_for(user)
    client.post(f"{URL}/{g.id}/join")
    assert client.post(f"{URL}/{g.id}/join").json()["code"] == "already_joined"


def test_join_blocked_with_participant(client_for, user):
    g = make_gathering(members=1)
    member = g.participations.exclude(user=g.creator).get().user
    Block.objects.create(blocker=member, blocked=user)
    r = client_for(user).post(f"{URL}/{g.id}/join")
    assert r.status_code == 403
    assert r.json()["code"] == "blocked"


def test_join_started_gathering(client_for, user):
    g = make_gathering()
    Gathering.objects.filter(pk=g.pk).update(starts_at=timezone.now() - timedelta(minutes=5))
    assert client_for(user).post(f"{URL}/{g.id}/join").json()["code"] == "gathering_closed"


# --- выход ---


def test_leave_frees_seat_and_reopens(client_for, user):
    g = make_gathering(seats=3, members=1)
    client = client_for(user)
    client.post(f"{URL}/{g.id}/join")
    r = client.post(f"{URL}/{g.id}/leave")
    assert r.json()["status"] == "open"
    assert r.json()["participants_count"] == 2
    p = Participation.objects.get(gathering=g, user=user)
    assert p.left_at is not None and p.late_leave is False


def test_late_leave_flag(client_for, user):
    g = make_gathering(starts_at=timezone.now() + timedelta(hours=1, minutes=30))
    client = client_for(user)
    client.post(f"{URL}/{g.id}/join")
    client.post(f"{URL}/{g.id}/leave")
    assert Participation.objects.get(gathering=g, user=user).late_leave is True


def test_creator_leave_transfers_role_to_earliest(client_for):
    g = make_gathering(members=2)
    first_member = g.participations.exclude(user=g.creator).order_by("joined_at").first().user
    client_for(g.creator).post(f"{URL}/{g.id}/leave")
    g.refresh_from_db()
    assert g.creator == first_member
    assert Participation.objects.get(
        gathering=g, user=first_member, left_at__isnull=True
    ).is_creator
    assert Message.objects.filter(gathering=g, system_event="creator_changed").exists()


def test_last_participant_leave_cancels(client_for):
    g = make_gathering()
    r = client_for(g.creator).post(f"{URL}/{g.id}/leave")
    assert r.json()["status"] == "cancelled"


def test_rejoin_after_leave(client_for, user):
    g = make_gathering()
    client = client_for(user)
    client.post(f"{URL}/{g.id}/join")
    client.post(f"{URL}/{g.id}/leave")
    assert client.post(f"{URL}/{g.id}/join").status_code == 200
    assert Participation.objects.filter(gathering=g, user=user).count() == 2


def test_csrf_error_in_russian(user):
    from rest_framework.test import APIClient

    client = APIClient(enforce_csrf_checks=True)
    client.force_login(user)
    r = client.post(f"{URL}/{make_gathering().id}/join")
    assert r.status_code == 403
    assert r.json()["code"] == "csrf_failed"
