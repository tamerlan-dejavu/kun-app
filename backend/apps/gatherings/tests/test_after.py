"""«Я пришёл» и оценки после встречи."""

from datetime import timedelta

import pytest
from django.utils import timezone

from apps.gatherings.models import Attendance, Rating
from tests.factories import GatheringFactory, ParticipationFactory, UserFactory

pytestmark = pytest.mark.django_db
URL = "/api/v1/gatherings"


def started(hours_ago: float, members=2):
    g = GatheringFactory()
    g.starts_at = timezone.now() - timedelta(hours=hours_ago)
    g.save()
    users = [ParticipationFactory(gathering=g).user for _ in range(members)]
    return g, users


def test_attendance_in_window(client_for):
    g, (a, _) = started(hours_ago=1)
    client = client_for(a)
    assert client.post(f"{URL}/{g.id}/attendance").status_code == 204
    assert client.post(f"{URL}/{g.id}/attendance").status_code == 204  # повтор — без ошибки
    assert Attendance.objects.filter(gathering=g, user=a).count() == 1


@pytest.mark.parametrize("hours_ago, code", [(-1, "too_early"), (13, "too_late")])
def test_attendance_outside_window(client_for, hours_ago, code):
    g, (a, _) = started(hours_ago=hours_ago)
    assert client_for(a).post(f"{URL}/{g.id}/attendance").json()["code"] == code


def test_attendance_only_participant(client_for):
    g, _ = started(hours_ago=1)
    assert (
        client_for(UserFactory()).post(f"{URL}/{g.id}/attendance").json()["code"]
        == "not_participant"
    )


def test_ratings(client_for):
    g, (a, b) = started(hours_ago=2)
    client = client_for(a)
    body = {"ratings": [{"user_id": b.id, "value": "ok"}]}
    assert client.post(f"{URL}/{g.id}/ratings", body, format="json").status_code == 204
    # повторная оценка заменяет предыдущую
    body["ratings"][0]["value"] = "no_show"
    client.post(f"{URL}/{g.id}/ratings", body, format="json")
    assert Rating.objects.get(gathering=g, rater=a, ratee=b).value == "no_show"


def test_ratings_rules(client_for):
    g, (a, _) = started(hours_ago=2)
    client = client_for(a)

    def post(user_id):
        body = {"ratings": [{"user_id": user_id, "value": "ok"}]}
        return client.post(f"{URL}/{g.id}/ratings", body, format="json").json()["code"]

    assert post(a.id) == "rate_self"
    assert post(UserFactory().id) == "not_participant"
