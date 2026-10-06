"""Персональный подбор «Для тебя» (ТЗ, «Персональный подбор»).

Правила и веса, без машинного обучения: данных пилота для обучения модели не хватит.
Каждый сигнал добавляет к оценке сбора вес; самый весомый — это и есть объяснение в одну строку.

Сигналы:
- together        в сборе есть люди, с которыми ты уже был на встрече (оба отметили «Я пришёл»)
- attended        категория, на которую ты реально приходишь
- interest        категория совпадает с интересом из профиля (Interest.categories)
- common          общие интересы с участниками
- time_habit      сбор в то время суток, когда ты обычно выбираешься
- near            рядом (если передана геолокация)
- popular         сбор набирается — социальное доказательство; у новичков без истории вес выше
"""

from collections import Counter
from dataclasses import dataclass, field
from datetime import timedelta

from django.contrib.gis.geos import Point
from django.utils import timezone

from apps.common.time import ALMATY

from .models import Attendance, Gathering
from .selectors import blocked_user_ids, feed_queryset

HORIZON_DAYS = 7
HISTORY_DAYS = 180
LIMIT = 10

WEIGHTS = {
    "together": 2.5,  # за каждого знакомого, максимум 2
    "attended": 1.5,  # за каждую отметку в категории, максимум 3
    "interest": 2.0,
    "common": 0.5,  # за каждый общий интерес с участниками, максимум 4
    "time_habit": 1.0,
    "near_1_5km": 1.5,
    "near_4km": 0.75,
    "popular": 1.0,  # x заполненность сбора
    "popular_newcomer": 1.5,  # множитель для новичков без истории
    "today": 0.5,
    "two_days": 0.25,
}


def time_bucket(dt) -> str:
    hour = dt.astimezone(ALMATY).hour
    if 6 <= hour < 12:
        return "morning"
    if 12 <= hour < 17:
        return "day"
    if 17 <= hour < 23:
        return "evening"
    return "night"


@dataclass
class Scored:
    gathering: Gathering
    score: float = 0.0
    reasons: list[tuple[float, str, dict]] = field(default_factory=list)

    def add(self, weight: float, code: str | None = None, **params):
        self.score += weight
        if code:
            self.reasons.append((weight, code, params))

    @property
    def reason(self) -> dict:
        if not self.reasons:
            return {"code": "fresh", "params": {}}
        _, code, params = max(self.reasons, key=lambda r: r[0])
        return {"code": code, "params": params}


@dataclass
class Profile:
    """Что мы знаем о человеке — считается один раз на запрос."""

    interest_ids: set[int]
    interest_by_category: dict[int, str]  # категория -> название интереса (для пояснения)
    attended_by_category: Counter
    habit: str | None
    together: dict[int, str]  # user_id -> имя тех, с кем уже был на встрече
    has_history: bool


def build_profile(user) -> Profile:
    since = timezone.now() - timedelta(days=HISTORY_DAYS)

    interest_by_category: dict[int, str] = {}
    interests = user.interests.prefetch_related("categories")
    for interest in interests:
        for category in interest.categories.all():
            interest_by_category.setdefault(category.pk, interest.name)

    my_attendances = list(
        Attendance.objects.filter(user=user, gathering__starts_at__gte=since).select_related(
            "gathering"
        )
    )
    attended_by_category = Counter(a.gathering.category_id for a in my_attendances)
    buckets = Counter(time_bucket(a.gathering.starts_at) for a in my_attendances)
    habit = buckets.most_common(1)[0][0] if sum(buckets.values()) >= 2 else None

    # Те, с кем ты был на одной встрече (оба отметились)
    together = dict(
        Attendance.objects.filter(gathering__in=[a.gathering_id for a in my_attendances])
        .exclude(user=user)
        .values_list("user_id", "user__name")
    )

    return Profile(
        interest_ids=set(interests.values_list("pk", flat=True)),
        interest_by_category=interest_by_category,
        attended_by_category=attended_by_category,
        habit=habit,
        together=together,
        has_history=bool(my_attendances),
    )


def recommend(user, *, point: Point | None = None, limit: int = LIMIT) -> list[Scored]:
    now = timezone.now()
    profile = build_profile(user)

    candidates = list(
        feed_queryset(user, point=point)
        .filter(starts_at__lte=now + timedelta(days=HORIZON_DAYS))
        .filter(is_participant=False)
        .prefetch_related("participations__user__interests")
    )

    blocked = blocked_user_ids(user)
    today = now.astimezone(ALMATY).date()
    scored: list[Scored] = []

    for g in candidates:
        members = [p.user for p in g.participations.all() if p.left_at is None]
        member_ids = {m.pk for m in members}
        if member_ids & blocked:
            continue  # присоединиться всё равно нельзя

        s = Scored(g)

        known = [profile.together[m] for m in member_ids if m in profile.together]
        if known:
            s.add(WEIGHTS["together"] * min(len(known), 2), "together", name=known[0], n=len(known))

        attended = profile.attended_by_category.get(g.category_id, 0)
        if attended:
            s.add(
                WEIGHTS["attended"] * min(attended, 3),
                "attended",
                category=g.category.name,
                n=attended,
            )

        if g.category_id in profile.interest_by_category:
            s.add(
                WEIGHTS["interest"],
                "interest",
                interest=profile.interest_by_category[g.category_id],
            )

        member_interests = {i.pk for m in members for i in m.interests.all()}
        common = len(member_interests & profile.interest_ids)
        if common:
            s.add(WEIGHTS["common"] * min(common, 4), "common", n=common)

        if profile.habit and time_bucket(g.starts_at) == profile.habit:
            s.add(WEIGHTS["time_habit"], "time_habit", bucket=profile.habit)

        distance = getattr(g, "distance_m", None)
        if distance is not None:
            if distance <= 1500:
                s.add(WEIGHTS["near_1_5km"], "near", km=round(distance / 1000, 1))
            elif distance <= 4000:
                s.add(WEIGHTS["near_4km"], "near", km=round(distance / 1000, 1))

        fill = g.participants_count / g.seats
        popular = WEIGHTS["popular"] * fill
        if not profile.has_history:
            popular *= WEIGHTS["popular_newcomer"]
        if g.participants_count >= 2:
            s.add(popular, "popular", n=g.participants_count)
        else:
            s.add(popular)

        days = (g.starts_at.astimezone(ALMATY).date() - today).days
        if days == 0:
            s.add(WEIGHTS["today"])
        elif days <= 2:
            s.add(WEIGHTS["two_days"])

        scored.append(s)

    scored.sort(key=lambda x: (-x.score, x.gathering.starts_at))
    return scored[:limit]
