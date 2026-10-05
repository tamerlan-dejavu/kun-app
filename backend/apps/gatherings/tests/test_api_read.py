"""Лента, сбор целиком, публичная страница, мои сборы."""

from datetime import timedelta

import pytest
from django.contrib.gis.geos import Point
from django.utils import timezone

from apps.moderation.models import Block, UserSanction
from tests.factories import CategoryFactory, GatheringFactory, ParticipationFactory, UserFactory

pytestmark = pytest.mark.django_db
FEED = "/api/v1/gatherings"


def ids(response):
    return [g["id"] for g in response.json()["results"]]


def test_feed_requires_login(api_client):
    r = api_client.get(FEED)
    # SessionAuthentication не шлёт WWW-Authenticate, поэтому DRF отвечает 403, а не 401
    assert r.status_code == 403
    assert r.json() == {"code": "not_authenticated", "message": "Нужно войти"}


def test_feed_requires_onboarding(client_for):
    r = client_for(UserFactory(onboarding_completed_at=None)).get(FEED)
    assert r.status_code == 403
    assert r.json()["code"] == "onboarding_required"


def test_feed_shows_only_open_published_future(client_for, user):
    visible = GatheringFactory()
    GatheringFactory(moderation_status="pending")
    GatheringFactory(status="cancelled", cancelled_at=timezone.now())
    GatheringFactory(status="full")
    past = GatheringFactory()
    past.starts_at = timezone.now() - timedelta(hours=1)
    past.save()

    r = client_for(user).get(FEED)
    assert r.status_code == 200
    assert ids(r) == [visible.id]
    card = r.json()["results"][0]
    assert card["participants_count"] == 0
    assert "address" not in card and "phone" not in str(card)


def test_feed_hides_blocked_both_ways_and_banned(client_for, user):
    blocked_by_me, blocked_me, banned, ok = (
        UserFactory(),
        UserFactory(),
        UserFactory(),
        UserFactory(),
    )
    Block.objects.create(blocker=user, blocked=blocked_by_me)
    Block.objects.create(blocker=blocked_me, blocked=user)
    UserSanction.objects.create(user=banned, kind="ban", reason="x", created_by=ok)
    for creator in (blocked_by_me, blocked_me, banned):
        GatheringFactory(creator=creator)
    visible = GatheringFactory(creator=ok)

    assert ids(client_for(user).get(FEED)) == [visible.id]


def test_feed_filters_category_and_date(client_for, user):
    cinema = CategoryFactory(slug="cinema", name="Кино")
    now = timezone.now()
    in_2h = GatheringFactory(category=cinema, starts_at=now + timedelta(hours=2))
    in_5d = GatheringFactory(starts_at=now + timedelta(days=5))
    in_12d = GatheringFactory(starts_at=now + timedelta(days=12))
    client = client_for(user)

    assert ids(client.get(FEED, {"category": "cinema"})) == [in_2h.id]
    week = ids(client.get(FEED, {"date": "week"}))
    assert in_5d.id in week and in_12d.id not in week
    assert client.get(FEED, {"date": "yesterday"}).json()["code"] == "validation_error"


def test_feed_sorted_by_distance(client_for, user):
    narxoz = (76.874, 43.2215)
    far = GatheringFactory(location=Point(77.059, 43.1573, srid=4326))  # Медеу
    near = GatheringFactory(location=Point(76.875, 43.222, srid=4326))
    r = client_for(user).get(FEED, {"lng": narxoz[0], "lat": narxoz[1]})
    assert ids(r) == [near.id, far.id]
    assert r.json()["results"][0]["distance_m"] < 200


def test_detail_has_address_and_participants(client_for, user):
    g = GatheringFactory()
    ParticipationFactory(gathering=g, user=g.creator, is_creator=True)
    r = client_for(user).get(f"{FEED}/{g.id}")
    assert r.status_code == 200
    data = r.json()
    assert data["address"] == g.address
    assert data["participants"][0]["is_creator"] is True
    assert "phone" not in data["participants"][0]["user"]
    assert data["is_participant"] is False


def test_pending_visible_only_to_creator(client_for, user):
    g = GatheringFactory(moderation_status="pending")
    assert client_for(user).get(f"{FEED}/{g.id}").status_code == 404
    assert client_for(g.creator).get(f"{FEED}/{g.id}").status_code == 200


def test_public_page_without_personal_data(api_client):
    g = GatheringFactory()
    ParticipationFactory(gathering=g, user=g.creator, is_creator=True)
    r = api_client.get(f"/api/v1/public/gatherings/{g.slug}")
    assert r.status_code == 200
    data = r.json()
    assert data["participants_count"] == 1
    for secret in ("address", "creator", "participants", "comment", "lat", "lng"):
        assert secret not in data
    hidden = GatheringFactory(moderation_status="hidden")
    assert api_client.get(f"/api/v1/public/gatherings/{hidden.slug}").status_code == 404


def test_my_gatherings_upcoming_and_past(client_for, user):
    upcoming = ParticipationFactory(user=user).gathering
    past = GatheringFactory(status="finished")
    ParticipationFactory(user=user, gathering=past)
    left = ParticipationFactory(user=user, left_at=timezone.now()).gathering

    client = client_for(user)
    assert ids(client.get("/api/v1/me/gatherings")) == [upcoming.id]
    assert ids(client.get("/api/v1/me/gatherings", {"when": "past"})) == [past.id]
    assert left.id not in ids(client.get("/api/v1/me/gatherings"))
