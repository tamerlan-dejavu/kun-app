"""Публичная витрина города для главной (без входа).

Гостю по ТЗ видно только: категория, название, время, район, «идут N из M» — без имён, фото
и точного адреса. Поэтому здесь:
- сборы — без места и людей;
- места — агрегат «где собираются», не привязанный ко времени конкретного сбора;
- люди — анонимно: сколько ищут компанию и какие у них интересы;
- точки карты — координаты огрублены до ~1 км.
"""

from collections import Counter
from datetime import timedelta

from django.db.models import Count, Q
from django.utils import timezone

from apps.catalog.models import Interest
from apps.common.time import ALMATY

from .models import Gathering, Participation
from .selectors import ACTIVE_PARTICIPATION

COORD_PRECISION = 2  # 0.01° ≈ 1.1 км по широте — район, а не дом
TODAY_LIMIT = 8
PLACES_LIMIT = 5
PEOPLE_LIMIT = 6


def _open_upcoming():
    return (
        Gathering.objects.filter(
            status=Gathering.Status.OPEN,
            moderation_status=Gathering.ModerationStatus.PUBLISHED,
            starts_at__gt=timezone.now(),
        )
        .select_related("category")
        .annotate(participants_count=Count("participations", filter=ACTIVE_PARTICIPATION))
    )


def _card(g) -> dict:
    return {
        "slug": g.slug,
        "title": g.title,
        "category": {"slug": g.category.slug, "name": g.category.name, "emoji": g.category.emoji},
        "starts_at": g.starts_at,
        "district": g.district,
        "seats": g.seats,
        "participants_count": g.participants_count,
    }


def city_snapshot() -> dict:
    now = timezone.now()
    local = now.astimezone(ALMATY)
    end_of_today = local.replace(hour=23, minute=59, second=59)

    upcoming = list(_open_upcoming().order_by("starts_at")[:60])
    today = [g for g in upcoming if g.starts_at <= end_of_today]
    # Сегодня пусто — показываем ближайшие, чтобы раздел не был пустым
    schedule = (today or upcoming)[:TODAY_LIMIT]

    # Люди: участники открытых сборов со свободными местами — анонимно, только интересы
    looking = [g for g in upcoming if g.participants_count < g.seats][:PEOPLE_LIMIT]
    people = []
    for g in looking:
        member_ids = Participation.objects.filter(gathering=g, left_at__isnull=True).values(
            "user_id"
        )
        interests = Counter(
            Interest.objects.filter(users__in=member_ids).values_list("name", flat=True)
        )
        people.append(
            {
                **_card(g),
                "free_seats": g.seats - g.participants_count,
                "interests": [name for name, _ in interests.most_common(3)],
            }
        )

    # Места: где чаще всего собираются за последние 60 дней (без времени и людей)
    places = (
        Gathering.objects.filter(
            moderation_status=Gathering.ModerationStatus.PUBLISHED,
            created_at__gte=now - timedelta(days=60),
        )
        .exclude(status=Gathering.Status.CANCELLED)
        .values("place_name", "district")
        .annotate(
            gatherings=Count("id"),
            upcoming=Count("id", filter=Q(starts_at__gt=now, status=Gathering.Status.OPEN)),
        )
        .order_by("-gatherings", "place_name")[:PLACES_LIMIT]
    )

    points = [
        {
            "slug": g.slug,
            "title": g.title,
            "emoji": g.category.emoji,
            "lat": round(g.location.y, COORD_PRECISION),
            "lng": round(g.location.x, COORD_PRECISION),
        }
        for g in upcoming
    ]

    return {
        "date": local.date(),
        "is_today": bool(today),
        "open_count": len(upcoming),
        "today_count": len(today),
        "schedule": [_card(g) for g in schedule],
        "people": people,
        "places": list(places),
        "points": points,
    }
