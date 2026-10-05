from django.db import models


class NotificationSettings(models.Model):
    """Переключатели по типам; отмену выключить нельзя.

    joined_left, chat_message, reminder, updated, after_prompt — bool.
    """

    # TODO: user OneToOne, флаги


class PushSubscription(models.Model):
    """Подписка Web Push (endpoint, p256dh, auth). Этап 3 — токены APNs/FCM (kind)."""

    # TODO: user FK, kind, endpoint unique, keys JSON, user_agent, created_at


class TelegramLink(models.Model):
    """Привязка Telegram: одноразовый токен диплинка -> chat_id."""

    # TODO: user OneToOne, token, chat_id, linked_at
