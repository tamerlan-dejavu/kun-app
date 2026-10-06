"""Демо-данные для локальной разработки: `python manage.py seed_demo`.

Заполняет все основные таблицы, чтобы было что смотреть в DataGrip и админке.
Только при DEBUG. Повторно не запускается — для чистого старта пересоздайте БД (make reset-db).
"""

import random
from datetime import timedelta

from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import User
from apps.catalog.models import Category, Interest
from apps.chat.models import Message
from apps.gatherings.models import Attendance, Gathering, Participation, Rating
from apps.moderation.models import BannedWord, Block, ModerationLog, Report, UserSanction
from apps.notifications.models import NotificationSettings, TelegramLink
from apps.universities.models import University

DEMO_PHONE_PREFIX = "+7700000"
# Только для dev-входа на /api/v1/auth/dev/login/ (в prod входа по паролю нет)
DEMO_PASSWORD = "kun-demo"

NAMES = [
    "Айгерим", "Данияр", "Алина", "Тимур", "Мадина", "Арман", "Камила",
    "Ерлан", "Дана", "Санжар", "Аружан", "Нурлан",
]  # fmt: skip

# (место, адрес, район, lng, lat) — примерные точки в Алматы
PLACES = [
    ("Университет Нархоз", "ул. Жандосова, 55", "Ауэзовский", 76.8740, 43.2215),
    ("Центральный парк", "ул. Гоголя, 1", "Медеуский", 76.9670, 43.2590),
    ("Кок-Тобе", "ул. Омаровой, 35", "Медеуский", 76.9760, 43.2330),
    ("Арбат", "ул. Жибек Жолы", "Алмалинский", 76.9450, 43.2617),
    ("Ботанический сад", "ул. Тимирязева, 36Д", "Бостандыкский", 76.9126, 43.2218),
    ("Esentai Mall", "пр. Аль-Фараби, 77/8", "Бостандыкский", 76.9284, 43.2183),
    ("Mega Alma-Ata", "ул. Розыбакиева, 247А", "Бостандыкский", 76.8920, 43.2016),
    ("Медеу", "ул. Горная, 465", "Медеуский", 77.0590, 43.1573),
]

# (категория, название, комментарий, сдвиг начала в часах, мест, статус, модерация)
GATHERINGS = [
    ("cinema", "Идём на новый Нолан", "Возьмём места в середине зала", 26, 4, "open", "published"),
    ("walk", "Вечерняя прогулка по Арбату", "", 6, 5, "open", "published"),
    (
        "board-games",
        "Настолки для новичков",
        "Научим играть в Каркассон",
        50,
        6,
        "open",
        "published",
    ),
    ("coffee", "Кофе после пар", "Просто поболтать", 3, 3, "full", "published"),
    ("sport", "Баскетбол 3х3", "Мяч есть", 74, 6, "open", "published"),
    ("concert", "Джаз в парке", "", 120, 4, "open", "pending"),
    ("walk", "Подъём на Кок-Тобе", "Пешком по тропе", 30, 5, "cancelled", "published"),
    ("food", "Плов в Медеу", "", -48, 4, "finished", "published"),
    ("study", "Готовимся к сессии", "Матан, берите конспекты", -120, 3, "finished", "published"),
]

CHAT_LINES = [
    "Привет всем! Я буду в серой куртке",
    "Отлично, увидимся у входа",
    "Опоздаю минут на 5, не уходите",
    "Кто-то уже на месте?",
    "Я тут, у фонтана",
]


class Command(BaseCommand):
    help = "Заполнить БД демо-данными (только DEBUG)"

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("seed_demo только для локальной разработки (DEBUG=True)")
        if User.objects.filter(phone__startswith=DEMO_PHONE_PREFIX).exists():
            self.stdout.write(
                self.style.WARNING("Демо-данные уже есть. Чистый старт: make reset-db")
            )
            return

        random.seed(42)
        with transaction.atomic():
            users = self._users()
            gatherings = self._gatherings(users)
            self._moderation(users, gatherings)

        self.stdout.write(
            self.style.SUCCESS(
                f"Готово: {len(users)} пользователей, {len(gatherings)} сборов, "
                f"{Message.objects.count()} сообщений"
            )
        )
        self.stdout.write(
            f"Вход: /api/v1/auth/dev/login/ — {users[1].phone} / {DEMO_PASSWORD} "
            f"(модератор: {users[0].phone})"
        )

    def _users(self):
        interests = list(Interest.objects.all())
        universities = list(University.objects.all())
        now = timezone.now()
        users = []
        for i, name in enumerate(NAMES):
            joined = now - timedelta(days=random.randint(3, 40))
            user = User.objects.create_user(
                phone=f"{DEMO_PHONE_PREFIX}{i:04d}",
                password=DEMO_PASSWORD,
                name=name,
                university=random.choice(universities) if i % 3 else None,
                role=User.Role.MODERATOR if i == 0 else User.Role.USER,
                adult_confirmed_at=joined,
                terms_accepted_at=joined,
                onboarding_completed_at=joined,
                date_joined=joined,
            )
            user.interests.set(random.sample(interests, random.randint(3, 5)))
            NotificationSettings.objects.create(user=user, chat_message=i % 4 != 0)
            if i % 2 == 0:
                TelegramLink.objects.create(user=user, chat_id=100_000 + i, linked_at=joined)
            users.append(user)
        return users

    def _gatherings(self, users):
        now = timezone.now()
        categories = {c.slug: c for c in Category.objects.all()}
        gatherings = []
        for idx, (cat, title, comment, hours, seats, status, moderation) in enumerate(GATHERINGS):
            place_name, address, district, lng, lat = PLACES[idx % len(PLACES)]
            creator = users[(idx + 1) % len(users)]
            starts_at = now + timedelta(hours=hours)
            g = Gathering.objects.create(
                creator=creator,
                category=categories[cat],
                title=title,
                comment=comment,
                place_name=place_name,
                address=address,
                district=district,
                place_external_id=f"demo-{idx}",
                location=Point(lng, lat, srid=4326),
                starts_at=starts_at,
                seats=seats,
                status=status,
                moderation_status=moderation,
                cancel_reason="Плохая погода, перенесём" if status == "cancelled" else "",
                cancelled_at=now - timedelta(hours=1) if status == "cancelled" else None,
            )
            gatherings.append(g)

            # Участники: создатель + другие (full — до упора)
            others = [u for u in users if u != creator]
            random.shuffle(others)
            count = seats if status == "full" else random.randint(1, seats - 1)
            members = [creator, *others[: count - 1]]
            for m in members:
                Participation.objects.create(gathering=g, user=m, is_creator=(m == creator))
                Message.objects.create(
                    gathering=g,
                    kind=Message.Kind.SYSTEM,
                    system_event=Message.SystemEvent.JOINED,
                    payload={"user_id": m.pk, "name": m.name},
                )
            # Один поздний выход в открытом сборе
            if status == "open" and len(others) > count:
                leaver = others[count]
                Participation.objects.create(
                    gathering=g,
                    user=leaver,
                    left_at=starts_at - timedelta(hours=1),
                    late_leave=True,
                )

            for line in random.sample(CHAT_LINES, random.randint(1, 4)):
                Message.objects.create(gathering=g, author=random.choice(members), text=line)

            if status == "cancelled":
                Message.objects.create(
                    gathering=g,
                    kind=Message.Kind.SYSTEM,
                    system_event=Message.SystemEvent.CANCELLED,
                    payload={"reason": g.cancel_reason},
                )

            # Прошедшие: отметки «Я пришёл» и оценки
            if status == "finished":
                came = members[:-1] if len(members) > 2 else members
                for m in came:
                    Attendance.objects.create(gathering=g, user=m)
                for rater in came:
                    for ratee in members:
                        if ratee != rater:
                            value = Rating.Value.OK if ratee in came else Rating.Value.NO_SHOW
                            Rating.objects.create(
                                gathering=g, rater=rater, ratee=ratee, value=value
                            )
                for m in came:
                    m.happened_gatherings_count += 1
                    m.reliability = 1.0
                    m.save(update_fields=["happened_gatherings_count", "reliability"])
        return gatherings

    def _moderation(self, users, gatherings):
        moderator = users[0]
        for word in ["казино", "ставки", "закладка"]:
            BannedWord.objects.create(word=word)

        offender, victim = users[5], users[6]
        message = Message.objects.create(
            gathering=gatherings[0], author=offender, text="Пишите в личку, есть дело"
        )
        Report.objects.create(
            reporter=victim,
            target_type=Report.TargetType.MESSAGE,
            target_message=message,
            reason=Report.Reason.SPAM,
            text="Зазывает в личку",
            priority=Report.Priority.HIGH,
        )
        Report.objects.create(
            reporter=users[7],
            target_type=Report.TargetType.USER,
            target_user=offender,
            reason=Report.Reason.NO_SHOW,
            status=Report.Status.RESOLVED,
            assigned_to=moderator,
            resolution_note="Предупреждение",
            resolved_at=timezone.now(),
        )
        Block.objects.create(blocker=victim, blocked=offender)
        sanction = UserSanction.objects.create(
            user=offender,
            kind=UserSanction.Kind.WARNING,
            reason="Спам в чате сбора",
            created_by=moderator,
        )
        ModerationLog.objects.create(
            actor=moderator,
            action=ModerationLog.Action.WARN,
            target_type="user",
            target_id=offender.pk,
            reason=sanction.reason,
        )
