"""Типы уведомлений (раздел 3.5 ТЗ)."""

from enum import StrEnum


class NotificationType(StrEnum):
    JOINED_LEFT = "joined_left"  # создателю
    CHAT_MESSAGE = "chat_message"  # участникам, не чаще 1 раза в 10 минут
    REMINDER = "reminder"  # за 2 часа
    UPDATED = "updated"  # сбор изменён
    CANCELLED = "cancelled"  # нельзя выключить; SMS, если < 3 часов
    AFTER_PROMPT = "after_prompt"  # «Как прошла встреча?» через 1 час
