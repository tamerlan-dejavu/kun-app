"""Метрика подбора (ТЗ): доля «присоединился -> пришёл» из «Для тебя» выше, чем из ленты.

    python manage.py recommendation_report --days 28

Считаем только прошедшие сборы, у которых закрылось окно «Я пришёл» (+12 ч после начала).
"""

from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Count, Exists, OuterRef, Q
from django.utils import timezone

from apps.gatherings.models import Attendance, Participation


class Command(BaseCommand):
    help = "Конверсия «присоединился -> пришёл» по источникам: Для тебя / Лента / Карта / Ссылка"

    def add_arguments(self, parser):
        parser.add_argument(
            "--days", type=int, default=28, help="за сколько дней (по началу сбора)"
        )

    def handle(self, *args, days, **options):
        now = timezone.now()
        closed = now - timedelta(hours=settings.KUN["ATTENDANCE_WINDOW_HOURS"])
        came = Attendance.objects.filter(gathering=OuterRef("gathering"), user=OuterRef("user"))
        rows = (
            Participation.objects.filter(
                gathering__starts_at__gte=now - timedelta(days=days),
                gathering__starts_at__lte=closed,
                left_at__isnull=True,
            )
            .exclude(is_creator=True)  # создатель не «приходит» из ленты — он её источник
            .annotate(came=Exists(came))
            .values("source")
            .annotate(joined=Count("id"), attended=Count("id", filter=Q(came=True)))
            .order_by("source")
        )

        labels = dict(Participation.Source.choices)
        self.stdout.write(f"Сборы за {days} дн., окно отметки закрыто\n")
        self.stdout.write(f"{'источник':<18}{'присоединились':>16}{'пришли':>9}{'конверсия':>11}")
        for r in rows:
            rate = r["attended"] / r["joined"] * 100 if r["joined"] else 0
            label = labels.get(r["source"], r["source"])
            self.stdout.write(f"{label:<18}{r['joined']:>16}{r['attended']:>9}{rate:>10.0f}%")
        if not rows:
            self.stdout.write("Пока нет данных: нужны прошедшие сборы с участниками.")
