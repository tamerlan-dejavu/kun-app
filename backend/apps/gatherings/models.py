from django.conf import settings
from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import F, Q

from apps.common.models import TimeStampedModel

from .slugs import generate_slug

SEATS_MIN = 3
SEATS_MAX = 6


class Gathering(TimeStampedModel):
    """Сбор: что, где, когда, сколько мест (разделы 3.3 и 6 ТЗ)."""

    class Status(models.TextChoices):
        OPEN = "open", "Набор открыт"
        FULL = "full", "Мест нет"
        CANCELLED = "cancelled", "Отменён"
        FINISHED = "finished", "Прошёл"

    class ModerationStatus(models.TextChoices):
        PUBLISHED = "published", "Опубликован"
        PENDING = "pending", "На проверке"
        HIDDEN = "hidden", "Скрыт модератором"

    slug = models.CharField(
        "slug", max_length=16, unique=True, default=generate_slug, db_comment="ссылка /g/<slug>"
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_gatherings",
        verbose_name="создатель",
        db_comment="текущий создатель — роль может передаваться другому участнику",
    )
    category = models.ForeignKey(
        "catalog.Category",
        on_delete=models.PROTECT,
        related_name="gatherings",
        verbose_name="категория",
    )
    title = models.CharField("название", max_length=60)
    comment = models.CharField("комментарий", max_length=300, blank=True)

    # Место — только из поиска 2ГИС
    place_name = models.CharField("название места", max_length=200)
    address = models.CharField(
        "адрес", max_length=300, db_comment="точный адрес — только участникам"
    )
    district = models.CharField(
        "район", max_length=100, blank=True, db_comment="показывается гостям вместо адреса"
    )
    place_external_id = models.CharField(
        "id места в 2ГИС", max_length=64, db_comment="адрес выбран из поиска, не свободный ввод"
    )
    location = models.PointField(
        "координаты", geography=True, srid=4326, db_comment="для сортировки ленты по расстоянию"
    )

    starts_at = models.DateTimeField("начало", db_comment="UTC; создание — от +1 ч до +14 дней")
    seats = models.PositiveSmallIntegerField(
        "мест всего",
        validators=[MinValueValidator(SEATS_MIN), MaxValueValidator(SEATS_MAX)],
        db_comment="3–6, включая создателя",
    )
    status = models.CharField("статус", max_length=16, choices=Status.choices, default=Status.OPEN)
    moderation_status = models.CharField(
        "модерация",
        max_length=16,
        choices=ModerationStatus.choices,
        default=ModerationStatus.PUBLISHED,
        db_comment="pending — сработал фильтр запрещённых слов",
    )
    cancel_reason = models.CharField("причина отмены", max_length=300, blank=True)
    cancelled_at = models.DateTimeField("отменён", null=True, blank=True)

    # Отметки фоновых задач (Celery) — чтобы не слать повторно и подводить итог один раз
    reminder_sent_at = models.DateTimeField("напоминание отправлено", null=True, blank=True)
    after_prompt_sent_at = models.DateTimeField(
        "«Как прошла встреча?» отправлено", null=True, blank=True
    )
    happened = models.BooleanField(
        "состоялся",
        null=True,
        blank=True,
        db_comment="итог через 12 ч после начала: >= 2 отметок «Я пришёл»; NULL — ещё не подведён",
    )
    settled_at = models.DateTimeField("итог подведён", null=True, blank=True)

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="Participation",
        related_name="gatherings",
        verbose_name="участники",
    )

    class Meta:
        verbose_name = "сбор"
        verbose_name_plural = "сборы"
        db_table_comment = "Сборы: что, где, когда, сколько мест"
        indexes = [
            # Лента: открытые опубликованные по времени начала
            models.Index(
                fields=["starts_at"],
                name="gathering_feed",
                condition=Q(status="open", moderation_status="published"),
            ),
            models.Index(fields=["creator", "status"], name="gathering_creator_status"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(seats__gte=SEATS_MIN, seats__lte=SEATS_MAX),
                name="gathering_seats_3_6",
            ),
            models.CheckConstraint(
                condition=~Q(status="cancelled") | Q(cancelled_at__isnull=False),
                name="gathering_cancelled_has_date",
            ),
        ]

    def __str__(self):
        return f"{self.title} ({self.starts_at:%d.%m %H:%M})"


class Participation(models.Model):
    """Участие в сборе. Выход не удаляет строку, а ставит left_at; повторный вход — новая строка."""

    class Source(models.TextChoices):
        FEED = "feed", "Лента"
        FOR_YOU = "for_you", "Для тебя"
        MAP = "map", "Карта"
        LINK = "link", "Ссылка / другое"

    gathering = models.ForeignKey(
        Gathering, on_delete=models.CASCADE, related_name="participations"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="participations"
    )
    is_creator = models.BooleanField("создатель", default=False)
    joined_at = models.DateTimeField("присоединился", auto_now_add=True)
    left_at = models.DateTimeField("вышел", null=True, blank=True)
    source = models.CharField(
        "откуда пришёл",
        max_length=16,
        choices=Source.choices,
        default=Source.LINK,
        db_comment="для метрики ТЗ: конверсия «Для тебя» -> «Я пришёл» против ленты",
    )
    late_leave = models.BooleanField(
        "поздний выход",
        default=False,
        db_comment="вышел менее чем за 2 ч до начала — снижает надёжность",
    )

    class Meta:
        verbose_name = "участие"
        verbose_name_plural = "участия"
        db_table_comment = "Участники сборов; left_at IS NULL — сейчас в сборе"
        constraints = [
            # Один активный участник на сбор (повторно — после выхода)
            models.UniqueConstraint(
                fields=["gathering", "user"],
                condition=Q(left_at__isnull=True),
                name="participation_one_active",
            ),
            # Один активный создатель на сбор
            models.UniqueConstraint(
                fields=["gathering"],
                condition=Q(is_creator=True, left_at__isnull=True),
                name="participation_one_creator",
            ),
        ]

    def __str__(self):
        return f"{self.user} в {self.gathering}"


class Attendance(models.Model):
    """Отметка «Я пришёл»: от начала до +12 часов.
    Вместе с категорией сбора и временем — основа персонального подбора (этап 2)."""

    gathering = models.ForeignKey(Gathering, on_delete=models.CASCADE, related_name="attendances")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="attendances"
    )
    marked_at = models.DateTimeField("отмечено", auto_now_add=True)

    class Meta:
        verbose_name = "отметка «Я пришёл»"
        verbose_name_plural = "отметки «Я пришёл»"
        db_table_comment = "Отметки «Я пришёл»; сбор состоялся, если их >= 2"
        constraints = [
            models.UniqueConstraint(fields=["gathering", "user"], name="attendance_once"),
        ]

    def __str__(self):
        return f"{self.user} пришёл на {self.gathering}"


class Rating(models.Model):
    """Оценка участника после встречи. Оцениваемый не видит автора."""

    class Value(models.TextChoices):
        OK = "ok", "Пришёл, всё хорошо"
        NO_SHOW = "no_show", "Не пришёл"

    gathering = models.ForeignKey(Gathering, on_delete=models.CASCADE, related_name="ratings")
    rater = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ratings_given",
        verbose_name="кто оценил",
        db_comment="никогда не отдаётся оцениваемому",
    )
    ratee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ratings_received",
        verbose_name="кого оценили",
    )
    value = models.CharField("оценка", max_length=16, choices=Value.choices)
    created_at = models.DateTimeField("создана", auto_now_add=True)

    class Meta:
        verbose_name = "оценка"
        verbose_name_plural = "оценки"
        db_table_comment = "Оценки участников после встречи: ok / no_show"
        constraints = [
            models.UniqueConstraint(
                fields=["gathering", "rater", "ratee"], name="rating_once_per_pair"
            ),
            models.CheckConstraint(condition=~Q(rater=F("ratee")), name="rating_not_self"),
        ]

    def __str__(self):
        return f"{self.ratee}: {self.value}"
