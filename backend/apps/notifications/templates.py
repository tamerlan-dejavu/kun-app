"""Тексты уведомлений — на «ты», коротко, без канцелярита (раздел 7 ТЗ).

TODO: вынести в gettext вместе с казахским (этап 2).
"""

from django.conf import settings
from django.utils import timezone

from .types import NotificationType as T


def _when(iso: str) -> str:
    from datetime import datetime

    return timezone.localtime(datetime.fromisoformat(iso)).strftime("%d.%m в %H:%M")


def render(ntype: str, ctx: dict) -> dict:
    """-> {title, body, url}. ctx собирает dispatcher.gathering_context()."""
    title = ctx.get("title", "")
    url = f"{settings.SITE_URL}/g/{ctx.get('slug', '')}"
    match ntype:
        case T.JOINED_LEFT:
            verb = "присоединился к сбору" if ctx.get("joined") else "вышел из сбора"
            body = f"{ctx.get('actor', 'Кто-то')} {verb} «{title}»"
        case T.CHAT_MESSAGE:
            body = f"Новые сообщения в чате «{title}»"
            url += "/chat"
        case T.REMINDER:
            body = f"Через 2 часа — «{title}», {ctx.get('place', '')}. Не опаздывай!"
        case T.UPDATED:
            when, place = _when(ctx["starts_at"]), ctx.get("place", "")
            body = f"Сбор «{title}» изменился. Теперь: {when}, {place}"
        case T.CANCELLED:
            reason = ctx.get("reason")
            body = f"Сбор «{title}» отменён" + (f": {reason}" if reason else "")
        case T.AFTER_PROMPT:
            body = f"Как прошла встреча «{title}»? Отметь, что ты пришёл, и оцени остальных"
            url += "/after"
        case _:
            body = title
    return {"title": "KUN", "body": body, "url": url}
