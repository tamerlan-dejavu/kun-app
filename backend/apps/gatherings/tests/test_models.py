"""Ограничения модели данных сборов — проверяются самой PostgreSQL."""

import pytest
from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.gatherings.models import Attendance, Rating
from apps.gatherings.slugs import ALPHABET, SLUG_LENGTH
from tests.factories import GatheringFactory, ParticipationFactory, UserFactory

pytestmark = pytest.mark.django_db


def assert_db_rejects(fn):
    with pytest.raises(IntegrityError), transaction.atomic():
        fn()


def test_slug_generated():
    g = GatheringFactory()
    assert len(g.slug) == SLUG_LENGTH
    assert set(g.slug) <= set(ALPHABET)


@pytest.mark.parametrize("seats", [2, 7])
def test_seats_outside_3_6_rejected(seats):
    assert_db_rejects(lambda: GatheringFactory(seats=seats))


def test_cancelled_requires_cancelled_at():
    assert_db_rejects(lambda: GatheringFactory(status="cancelled"))
    GatheringFactory(status="cancelled", cancelled_at=timezone.now())


def test_one_active_participation_per_user():
    p = ParticipationFactory()
    assert_db_rejects(lambda: ParticipationFactory(gathering=p.gathering, user=p.user))


def test_rejoin_after_leave_allowed():
    p = ParticipationFactory()
    p.left_at = timezone.now()
    p.save()
    ParticipationFactory(gathering=p.gathering, user=p.user)


def test_one_active_creator():
    p = ParticipationFactory(is_creator=True)
    assert_db_rejects(lambda: ParticipationFactory(gathering=p.gathering, is_creator=True))


def test_attendance_once():
    p = ParticipationFactory()
    Attendance.objects.create(gathering=p.gathering, user=p.user)
    assert_db_rejects(lambda: Attendance.objects.create(gathering=p.gathering, user=p.user))


def test_rating_not_self_and_once():
    g = GatheringFactory()
    a, b = UserFactory(), UserFactory()
    assert_db_rejects(lambda: Rating.objects.create(gathering=g, rater=a, ratee=a, value="ok"))
    Rating.objects.create(gathering=g, rater=a, ratee=b, value="ok")
    assert_db_rejects(lambda: Rating.objects.create(gathering=g, rater=a, ratee=b, value="no_show"))
