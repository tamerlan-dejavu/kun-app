from django.conf import settings
from django.db import models
from django.db.models import F, Q


class Report(models.Model):
    """Жалоба на пользователя, сбор или сообщение (раздел 3.7 ТЗ).
    Заполнена ровно одна цель — та, что указана в target_type."""

    class TargetType(models.TextChoices):
        USER = "user", "Пользователь"
        GATHERING = "gathering", "Сбор"
        MESSAGE = "message", "Сообщение"

    # TODO: согласовать список и приоритеты с вкладкой «Безопасность» документов MVP
    class Reason(models.TextChoices):
        SPAM = "spam", "Спам или реклама"
        HARASSMENT = "harassment", "Оскорбления, травля"
        INAPPROPRIATE = "inappropriate", "Неприемлемый контент"
        DANGER = "danger", "Угроза безопасности"
        UNDERAGE = "underage", "Похоже, младше 18"
        FAKE = "fake", "Фейковый профиль"
        NO_SHOW = "no_show", "Не пришёл, не предупредил"
        OTHER = "other", "Другое"

    class Priority(models.TextChoices):
        CRITICAL = "critical", "Критичная"
        HIGH = "high", "Высокая"
        NORMAL = "normal", "Обычная"

    class Status(models.TextChoices):
        NEW = "new", "Новая"
        IN_REVIEW = "in_review", "В работе"
        RESOLVED = "resolved", "Принято решение"
        REJECTED = "rejected", "Отклонена"

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="reports_sent",
        verbose_name="автор жалобы",
    )
    target_type = models.CharField("на что", max_length=16, choices=TargetType.choices)
    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reports_received",
    )
    target_gathering = models.ForeignKey(
        "gatherings.Gathering",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reports",
    )
    target_message = models.ForeignKey(
        "chat.Message", on_delete=models.CASCADE, null=True, blank=True, related_name="reports"
    )
    reason = models.CharField("причина", max_length=32, choices=Reason.choices)
    text = models.CharField("комментарий", max_length=1000, blank=True)
    priority = models.CharField(
        "приоритет",
        max_length=16,
        choices=Priority.choices,
        default=Priority.NORMAL,
        db_comment="critical сразу дублируется в Telegram-чат модераторов",
    )
    status = models.CharField("статус", max_length=16, choices=Status.choices, default=Status.NEW)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reports_assigned",
        verbose_name="модератор",
    )
    resolution_note = models.TextField("решение", blank=True)
    created_at = models.DateTimeField("создана", auto_now_add=True)
    resolved_at = models.DateTimeField("закрыта", null=True, blank=True)

    class Meta:
        verbose_name = "жалоба"
        verbose_name_plural = "жалобы"
        db_table_comment = "Жалобы на пользователей, сборы и сообщения"
        indexes = [
            # Очередь модератора: открытые жалобы по приоритету и времени
            models.Index(
                fields=["priority", "created_at"],
                name="report_queue",
                condition=Q(status__in=["new", "in_review"]),
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(
                        target_type="user",
                        target_user__isnull=False,
                        target_gathering__isnull=True,
                        target_message__isnull=True,
                    )
                    | Q(
                        target_type="gathering",
                        target_user__isnull=True,
                        target_gathering__isnull=False,
                        target_message__isnull=True,
                    )
                    | Q(
                        target_type="message",
                        target_user__isnull=True,
                        target_gathering__isnull=True,
                        target_message__isnull=False,
                    )
                ),
                name="report_exactly_one_target",
            ),
        ]

    def __str__(self):
        return f"#{self.pk} {self.get_target_type_display()}: {self.get_reason_display()}"


class Block(models.Model):
    """Пользовательская блокировка: не видят сборы друг друга и не попадают в один сбор."""

    blocker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blocks_made",
        verbose_name="кто заблокировал",
    )
    blocked = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blocked_by",
        verbose_name="кого",
    )
    created_at = models.DateTimeField("создана", auto_now_add=True)

    class Meta:
        verbose_name = "блокировка"
        verbose_name_plural = "блокировки"
        db_table_comment = "Блокировки между пользователями (действуют в обе стороны)"
        constraints = [
            models.UniqueConstraint(fields=["blocker", "blocked"], name="block_once"),
            models.CheckConstraint(condition=~Q(blocker=F("blocked")), name="block_not_self"),
        ]

    def __str__(self):
        return f"{self.blocker} -> {self.blocked}"


class UserSanction(models.Model):
    """Санкция модератора: предупреждение, пауза 7 дней или бан."""

    class Kind(models.TextChoices):
        WARNING = "warning", "Предупреждение"
        PAUSE = "pause", "Пауза"
        BAN = "ban", "Блокировка"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sanctions"
    )
    kind = models.CharField("тип", max_length=16, choices=Kind.choices)
    reason = models.TextField("причина")
    ends_at = models.DateTimeField(
        "действует до", null=True, blank=True, db_comment="пауза — +7 дней; бан — NULL (бессрочно)"
    )
    revoked_at = models.DateTimeField("снята досрочно", null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="sanctions_given",
        verbose_name="модератор",
    )
    created_at = models.DateTimeField("назначена", auto_now_add=True)

    class Meta:
        verbose_name = "санкция"
        verbose_name_plural = "санкции"
        db_table_comment = "Санкции модераторов: warning / pause / ban"
        constraints = [
            models.CheckConstraint(
                condition=~Q(kind="pause") | Q(ends_at__isnull=False),
                name="sanction_pause_has_end",
            ),
        ]

    def __str__(self):
        return f"{self.user}: {self.get_kind_display()}"


class BannedWord(models.Model):
    """Запрещённое слово для автопроверки названия и комментария сбора."""

    word = models.CharField("слово", max_length=100, unique=True, db_comment="в нижнем регистре")
    is_active = models.BooleanField("активно", default=True)
    created_at = models.DateTimeField("добавлено", auto_now_add=True)

    class Meta:
        verbose_name = "запрещённое слово"
        verbose_name_plural = "запрещённые слова"
        ordering = ["word"]
        db_table_comment = "Список запрещённых слов: совпадение -> сбор на проверку"

    def __str__(self):
        return self.word

    def save(self, *args, **kwargs):
        self.word = self.word.strip().lower()
        super().save(*args, **kwargs)


class ModerationLog(models.Model):
    """Неизменяемый журнал действий модераторов: кто, что, причина, когда.

    UPDATE и DELETE запрещены триггером в БД (миграция moderation 0002), здесь — дублируем
    на уровне ORM, чтобы ошибка была понятной раньше.
    """

    class Action(models.TextChoices):
        HIDE_MESSAGE = "hide_message", "Скрыл сообщение"
        HIDE_GATHERING = "hide_gathering", "Скрыл сбор"
        PUBLISH_GATHERING = "publish_gathering", "Опубликовал сбор после проверки"
        WARN = "warn", "Предупредил"
        PAUSE = "pause", "Пауза 7 дней"
        BAN = "ban", "Заблокировал"
        REVOKE_SANCTION = "revoke_sanction", "Снял санкцию"
        RESOLVE_REPORT = "resolve_report", "Закрыл жалобу"
        REJECT_REPORT = "reject_report", "Отклонил жалобу"
        CHANGE_ROLE = "change_role", "Изменил роль"

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="moderation_actions",
        verbose_name="модератор",
    )
    action = models.CharField("действие", max_length=32, choices=Action.choices)
    target_type = models.CharField(
        "тип объекта", max_length=32, db_comment="user / gathering / message / report"
    )
    target_id = models.BigIntegerField("id объекта")
    reason = models.TextField("причина", db_comment="обязательна для любого действия")
    report = models.ForeignKey(
        Report,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="log_entries",
        verbose_name="по жалобе",
    )
    created_at = models.DateTimeField("когда", auto_now_add=True)

    class Meta:
        verbose_name = "запись журнала модерации"
        verbose_name_plural = "журнал модерации"
        ordering = ["-created_at"]
        db_table_comment = "Неизменяемый журнал модераторов: UPDATE/DELETE запрещены триггером"
        indexes = [models.Index(fields=["target_type", "target_id"], name="modlog_target")]
        constraints = [
            models.CheckConstraint(condition=~Q(reason=""), name="modlog_reason_required"),
        ]

    def __str__(self):
        return f"{self.created_at:%Y-%m-%d %H:%M} {self.actor}: {self.get_action_display()}"

    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise PermissionError("Журнал модерации нельзя изменять")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise PermissionError("Журнал модерации нельзя удалять")
