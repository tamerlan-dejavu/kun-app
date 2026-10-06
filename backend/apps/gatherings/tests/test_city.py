"""Публичная витрина города: что видно гостю и что — нет."""

from datetime import timedelta

import pytest
from django.contrib.gis.geos import Point
from django.utils import timezone

from apps.catalog.models import Interest
from tests.factories import GatheringFactory, ParticipationFactory, UserFactory

pytestmark = pytest.mark.django_db
URL = "/api/v1/public/city"


def test_guest_sees_city_without_personal_data(api_client):
    g = GatheringFactory(
        location=Point(76.87412, 43.22156, srid=4326),
        starts_at=timezone.now() + timedelta(hours=2),
    )
    member = UserFactory(name="Секретное Имя", phone="+77019998877")
    member.interests.set([Interest.objects.get(slug="music")])
    ParticipationFactory(gathering=g, user=member)

    r = api_client.get(URL)
    assert r.status_code == 200
    data = r.json()
    body = r.content.decode()

    # без имён, телефонов и точного адреса
    assert "Секретное Имя" not in body and "+77019998877" not in body
    assert g.address not in body
    assert "place_name" not in data["schedule"][0]

    # координаты огрублены до ~1 км
    point = data["points"][0]
    assert (point["lat"], point["lng"]) == (43.22, 76.87)

    # люди — анонимно, только интересы
    assert data["people"][0]["interests"] == ["Музыка"]
    assert data["people"][0]["free_seats"] == g.seats - 1


def test_schedule_falls_back_to_upcoming(api_client):
    GatheringFactory(starts_at=timezone.now() + timedelta(days=3))
    data = api_client.get(URL).json()
    assert data["today_count"] in (0, 1)  # «сегодня» по Алматы зависит от часа запуска
    assert len(data["schedule"]) == 1


def test_hidden_and_cancelled_not_shown(api_client):
    GatheringFactory(moderation_status="pending")
    GatheringFactory(status="cancelled", cancelled_at=timezone.now())
    data = api_client.get(URL).json()
    assert data["schedule"] == [] and data["points"] == []


def test_feed_has_exact_coordinates_for_logged_in(client_for, user):
    GatheringFactory(location=Point(76.87412, 43.22156, srid=4326))
    card = client_for(user).get("/api/v1/gatherings").json()["results"][0]
    assert (card["lat"], card["lng"]) == (43.22156, 76.87412)
