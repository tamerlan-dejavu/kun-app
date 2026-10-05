from django.conf import settings
from django.db import models


class NotificationSettings(models.Model):
    """Какие уведомления присылать. Отмену сбора выключить нельзя — для неё поля нет."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="notification_settings",
    )
    joined_left = models.BooleanField(
        "кто-то присоединился / вышел", default=True, db_comment="только создателю"
    )
    chat_message = models.BooleanField(
        "новое сообщение в чате", default=True, db_comment="не чаще 1 раза в 10 минут"
    )
    reminder = models.BooleanField("напоминание за 2 часа", default=True)
    updated = models.BooleanField("сбор изменён", default=True)
    after_prompt = models.BooleanField("«Как прошла встреча?»", default=True)
    updated_at = models.DateTimeField("изменено", auto_now=True)

    class Meta:
        verbose_name = "настройки уведомлений"
        verbose_name_plural = "настройки уведомлений"
        db_table_comment = "Переключатели уведомлений по типам (отмена — всегда включена)"

    def __str__(self):
        return f"Уведомления {self.user}"


class PushSubscription(models.Model):
    """Подписка на пуши: Web Push сейчас, APNs/FCM на этапе 3."""

    class Kind(models.TextChoices):
        WEBPUSH = "webpush", "Web Push"
        APNS = "apns", "APNs (iOS)"
        FCM = "fcm", "FCM (Android)"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="push_subscriptions"
    )
    kind = models.CharField("тип", max_length=16, choices=Kind.choices, default=Kind.WEBPUSH)
    endpoint = models.TextField(
        "endpoint / токен", unique=True, db_comment="URL Web Push или токен устройства"
    )
    keys = models.JSONField(
        "ключи", default=dict, blank=True, db_comment="p256dh и auth для Web Push"
    )
    user_agent = models.CharField("устройство", max_length=300, blank=True)
    created_at = models.DateTimeField("создана", auto_now_add=True)
    last_used_at = models.DateTimeField("последняя отправка", null=True, blank=True)

    class Meta:
        verbose_name = "подписка на пуши"
        verbose_name_plural = "подписки на пуши"
        db_table_comment = "Подписки Web Push (потом APNs/FCM)"

    def __str__(self):
        return f"{self.user} — {self.kind}"


class TelegramLink(models.Model):
    """Привязка Telegram-бота: /start <link_token> -> chat_id."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="telegram_link"
    )
    link_token = models.CharField(
        "токен диплинка",
        max_length=64,
        unique=True,
        null=True,
        blank=True,
        db_comment="одноразовый, обнуляется после привязки",
    )
    chat_id = models.BigIntegerField("chat_id", unique=True, null=True, blank=True)
    linked_at = models.DateTimeField("привязан", null=True, blank=True)
    created_at = models.DateTimeField("создана", auto_now_add=True)

    class Meta:
        verbose_name = "привязка Telegram"
        verbose_name_plural = "привязки Telegram"
        db_table_comment = "Привязка аккаунта к Telegram-боту уведомлений"

    def __str__(self):
        return f"{self.user} — {'привязан' if self.chat_id else 'ожидает'}"
