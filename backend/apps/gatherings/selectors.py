"""Запросы на чтение: видимость сборов, лента, мои сборы."""

from datetime import datetime, time, timedelta

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.db.models import Count, Exists, FloatField, OuterRef, Q, QuerySet
from django.db.models.functions import Cast
from django.utils import timezone

from apps.common.time import ALMATY
from apps.moderation.models import Block, UserSanction

from .models import Gathering, Participation

ACTIVE_PARTICIPATION = Q(participations__left_at__isnull=True)


def with_counts(qs: QuerySet, user=None) -> QuerySet:
    """«Идут N из M» и «я участник» — одним запросом, без N+1."""
    qs = qs.select_related("category").annotate(
        participants_count=Count("participations", filter=ACTIVE_PARTICIPATION, distinct=True)
    )
    if user is not None and user.is_authenticated:
        qs = qs.annotate(
            is_participant=Exists(
                Participation.objects.filter(
                    gathering=OuterRef("pk"), user=user, left_at__isnull=True
                )
            )
        )
    return qs


def blocked_user_ids(user) -> set[int]:
    """Пользователи, с которыми у user блокировка в любую сторону."""
    pairs = Block.objects.filter(Q(blocker=user) | Q(blocked=user)).values_list(
        "blocker_id", "blocked_id"
    )
    return {blocked if blocker == user.pk else blocker for blocker, blocked in pairs}


def visible_gatherings(user) -> QuerySet:
    """Что пользователь может открыть: опубликованное (свои — в любом статусе модерации),
    без сборов тех, с кем блокировка, и без создателей с действующим баном."""
    now = timezone.now()
    banned_creators = UserSanction.objects.filter(kind="ban", revoked_at__isnull=True).filter(
        Q(ends_at__isnull=True) | Q(ends_at__gt=now)
    )

    blocked = blocked_user_ids(user)
    return (
        Gathering.objects.filter(Q(moderation_status="published") | Q(creator=user))
        .exclude(creator_id__in=blocked)
        .exclude(creator_id__in=banned_creators.values("user_id"))
    )


def date_range(day: str, now: datetime) -> tuple[datetime, datetime]:
    """Сегодня / Завтра / На неделе — по календарю Алматы."""
    today = now.astimezone(ALMATY).date()
    start_of = lambda d: datetime.combine(d, time.min, tzinfo=ALMATY)  # noqa: E731
    if day == "today":
        return now, start_of(today + timedelta(days=1))
    if day == "tomorrow":
        return start_of(today + timedelta(days=1)), start_of(today + timedelta(days=2))
    return now, start_of(today + timedelta(days=8))  # week: сегодня + 7 дней


def feed_queryset(user, *, date=None, category=None, point: Point | None = None) -> QuerySet:
    """Лента: открытые опубликованные будущие сборы.
    Сортировка — по времени начала или по расстоянию (если передан point)."""
    now = timezone.now()
    qs = visible_gatherings(user).filter(
        status=Gathering.Status.OPEN,
        moderation_status=Gathering.ModerationStatus.PUBLISHED,
        starts_at__gt=now,
    )
    if date:
        start, end = date_range(date, now)
        qs = qs.filter(starts_at__gte=start, starts_at__lt=end)
    if category:
        qs = qs.filter(category__slug=category)
    qs = with_counts(qs, user)
    if point is not None:
        # Метры как float: курсорной пагинации нужно сравнимое значение
        qs = qs.annotate(distance_m=Cast(Distance("location", point), FloatField()))
    return qs


def my_gatherings(user, when: str = "upcoming") -> QuerySet:
    """Сборы, где пользователь сейчас участник. upcoming — ещё не прошли (и идущие сейчас),
    past — прошедшие и отменённые."""
    now = timezone.now()
    # pk__in, а не participations__user: фильтр по той же связи сломал бы Count в with_counts
    mine = Participation.objects.filter(user=user, left_at__isnull=True).values("gathering_id")
    qs = Gathering.objects.filter(pk__in=mine)
    active = Q(status__in=["open", "full"]) & Q(starts_at__gt=now - timedelta(hours=12))
    qs = qs.filter(active) if when == "upcoming" else qs.exclude(active)
    return with_counts(qs, user)
