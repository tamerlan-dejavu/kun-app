"""Telegram Bot API: уведомления пользователям и алерты в чат модераторов."""

import logging

import httpx
from django.conf import settings

logger = logging.getLogger(__name__)
API = "https://api.telegram.org/bot{token}/sendMessage"


def is_configured() -> bool:
    return bool(settings.TELEGRAM_BOT_TOKEN)


def send_message(chat_id: int | str, text: str, url: str | None = None) -> bool:
    """True — доставлено. Ошибки Telegram не роняют задачу: логируем и идём дальше."""
    payload = {"chat_id": chat_id, "text": text, "disable_web_page_preview": True}
    if url:
        payload["reply_markup"] = {"inline_keyboard": [[{"text": "Открыть в KUN", "url": url}]]}
    try:
        response = httpx.post(
            API.format(token=settings.TELEGRAM_BOT_TOKEN), json=payload, timeout=5
        )
        response.raise_for_status()
        return True
    except httpx.HTTPError as e:
        # Текст и chat_id не пишем — только факт ошибки
        logger.warning("telegram: не доставлено (%s)", type(e).__name__)
        return False
