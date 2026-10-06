"""Доставка уведомлений (Celery). Каналы: Telegram, Web Push, SMS (только отмена < 3 ч).

Если ни один канал не настроен (dev без ключей) — пишем уведомление в лог.
"""

import logging

from celery import shared_task

from apps.accounts.models import User

from .channels import sms as sms_channel
from .channels import telegram, webpush
from .models import PushSubscription, TelegramLink
from .templates import render

logger = logging.getLogger("kun.notifications")


@shared_task
def deliver(user_id: int, ntype: str, context: dict, sms: bool = False) -> list[str]:
    """-> список каналов, куда ушло (для тестов и отладки)."""
    user = User.objects.filter(pk=user_id, deleted_at__isnull=True).first()
    if user is None:
        return []
    message = render(ntype, context)
    sent = []

    if telegram.is_configured():
        link = TelegramLink.objects.filter(user=user, chat_id__isnull=False).first()
        if link and telegram.send_message(link.chat_id, message["body"], message["url"]):
            sent.append("telegram")

    if webpush.is_configured():
        for sub in PushSubscription.objects.filter(user=user, kind="webpush"):
            if webpush.send(sub, message):
                sent.append("webpush")
                break

    if sms:
        sms_channel.send(user, message["body"])
        sent.append("sms")

    if not sent:
        logger.info("[%s] user=%s: %s", ntype, user_id, message["body"])
        sent.append("log")
    return sent
