"""Подбор «Для тебя»: что поднимается выше и как объясняется."""

from datetime import timedelta

import pytest
from django.contrib.gis.geos import Point
from django.core.management import call_command
from django.utils import timezone

from apps.catalog.models import Category, Interest
from apps.gatherings.for_you import recommend, time_bucket
from apps.gatherings.models import Attendance, Gathering, Participation
from apps.moderation.models import Block
from tests.factories import GatheringFactory, ParticipationFactory, UserFactory

pytestmark = pytest.mark.django_db


def cat(slug):
    return Category.objects.get(slug=slug)


def upcoming(category="walk", hours=24, **kw):
    g = GatheringFactory(
        category=cat(category), starts_at=timezone.now() + timedelta(hours=hours), **kw
    )
    ParticipationFactory(gathering=g, user=g.creator, is_creator=True)
    return g


def past_together(me, other, category="board-games", hours_ago=48):
    """Прошедший сбор, где оба отметили «Я пришёл»."""
    g = GatheringFactory(category=cat(category), status="finished")
    Gathering.objects.filter(pk=g.pk).update(starts_at=timezone.now() - timedelta(hours=hours_ago))
    for u in (me, other):
        Participation.objects.create(gathering=g, user=u)
        Attendance.objects.create(gathering=g, user=u)
    return g


def reason(items, g):
    return next(s.reason for s in items if s.gathering.pk == g.pk)


def test_interest_ranks_higher_and_explains(user):
    user.interests.set([Interest.objects.get(slug="board-games")])
    boring = upcoming("sport")
    match = upcoming("board-games")
    items = recommend(user)
    assert [s.gathering.pk for s in items][:2] == [match.pk, boring.pk]
    assert reason(items, match) == {"code": "interest", "params": {"interest": "Настольные игры"}}


def test_people_you_met_beat_interest(user):
    friend = UserFactory(name="Тимур")
    past_together(user, friend)
    user.interests.set([Interest.objects.get(slug="movies")])
    by_interest = upcoming("cinema")
    with_friend = upcoming("walk")
    ParticipationFactory(gathering=with_friend, user=friend)

    items = recommend(user)
    assert items[0].gathering.pk == with_friend.pk
    r = reason(items, with_friend)
    assert r["code"] == "together" and r["params"]["name"] == "Тимур"
    assert by_interest.pk in [s.gathering.pk for s in items]


def test_attended_category_counts(user):
    for _ in range(2):
        past_together(user, UserFactory(), category="board-games")
    g = upcoming("board-games")
    r = reason(recommend(user), g)
    # «together» тоже есть, но знакомых в этом сборе нет — объясняет история категории
    assert r == {"code": "attended", "params": {"category": "Настолки", "n": 2}}


def test_time_habit():
    assert time_bucket(timezone.now().replace(hour=14)) in {"morning", "day", "evening", "night"}


def test_excludes_joined_full_blocked_and_far_future(user):
    joined = upcoming()
    ParticipationFactory(gathering=joined, user=user)
    full = upcoming(status="full")
    later = upcoming(hours=24 * 9)
    with_blocked = upcoming()
    enemy = UserFactory()
    ParticipationFactory(gathering=with_blocked, user=enemy)
    Block.objects.create(blocker=enemy, blocked=user)
    ok = upcoming()

    ids = {s.gathering.pk for s in recommend(user)}
    assert ok.pk in ids
    assert not ids & {joined.pk, full.pk, later.pk, with_blocked.pk}


def test_near_with_location(user):
    near = upcoming(location=Point(76.874, 43.2215, srid=4326))
    upcoming(location=Point(77.05, 43.16, srid=4326))
    items = recommend(user, point=Point(76.875, 43.222, srid=4326))
    assert items[0].gathering.pk == near.pk
    assert reason(items, near)["code"] == "near"


def test_endpoint(client_for, user):
    upcoming()
    r = client_for(user).get("/api/v1/for-you")
    assert r.status_code == 200
    item = r.json()[0]
    assert {"gathering", "reason"} <= item.keys()
    assert item["reason"]["code"] in {"popular", "fresh", "interest"}


def test_join_saves_source_and_report(client_for, user, capsys):
    g = upcoming()
    client_for(user).post(f"/api/v1/gatherings/{g.id}/join", {"source": "for_you"}, format="json")
    p = Participation.objects.get(gathering=g, user=user)
    assert p.source == "for_you"

    # Сбор прошёл, участник отметился — попадает в отчёт
    Gathering.objects.filter(pk=g.pk).update(starts_at=timezone.now() - timedelta(hours=20))
    Attendance.objects.create(gathering=g, user=user)
    call_command("recommendation_report", days=7)
    out = capsys.readouterr().out
    assert "Для тебя" in out and "100%" in out


def test_join_default_source_is_link(client_for, user):
    g = upcoming()
    client_for(user).post(f"/api/v1/gatherings/{g.id}/join")
    assert Participation.objects.get(gathering=g, user=user).source == "link"
