from django.conf import settings
from django.db import models
from django.db.models import Q

MESSAGE_MAX_LENGTH = 1000


class Message(models.Model):
    """Сообщение в чате сбора: только текст до 1000 символов (раздел 3.4 ТЗ)."""

    class Kind(models.TextChoices):
        USER = "user", "Сообщение участника"
        SYSTEM = "system", "Системное"

    class SystemEvent(models.TextChoices):
        JOINED = "joined", "Присоединился"
        LEFT = "left", "Вышел"
        UPDATED = "updated", "Сбор изменён"
        CANCELLED = "cancelled", "Сбор отменён"
        CREATOR_CHANGED = "creator_changed", "Сменился создатель"

    gathering = models.ForeignKey(
        "gatherings.Gathering", on_delete=models.CASCADE, related_name="messages"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="messages",
        db_comment="NULL у системных сообщений",
    )
    kind = models.CharField("тип", max_length=16, choices=Kind.choices, default=Kind.USER)
    system_event = models.CharField(
        "событие", max_length=32, choices=SystemEvent.choices, blank=True
    )
    text = models.CharField(
        "текст", max_length=MESSAGE_MAX_LENGTH, blank=True, db_comment="в логи не пишется"
    )
    payload = models.JSONField(
        "данные события", default=dict, blank=True, db_comment="для системных: кто, что изменилось"
    )
    is_hidden = models.BooleanField("скрыто модератором", default=False)
    hidden_at = models.DateTimeField("скрыто", null=True, blank=True)
    created_at = models.DateTimeField("отправлено", auto_now_add=True)

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"
        db_table_comment = "Чат сбора: сообщения участников и системные события"
        indexes = [models.Index(fields=["gathering", "-created_at"], name="message_history")]
        constraints = [
            models.CheckConstraint(
                condition=Q(kind="system", system_event__gt="") | Q(kind="user", system_event=""),
                name="message_system_event_matches_kind",
            ),
        ]

    def __str__(self):
        return f"{self.gathering_id}: {self.text[:40] or self.system_event}"
