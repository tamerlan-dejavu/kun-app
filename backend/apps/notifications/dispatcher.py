"""Кому и что отправить (раздел 3.5 ТЗ). Сама отправка — в Celery (tasks.deliver).

- Настройки пользователя: каждый тип можно выключить, кроме отмены.
- Чат: не чаще 1 раза в 10 минут на человека и сбор.
- Ставим в очередь только после коммита транзакции.
"""

from django.conf import settings
from django.core.cache import cache
from django.db import transaction

from .models import NotificationSettings
from .types import NotificationType as T

ALWAYS_ON = {T.CANCELLED}


def gathering_context(gathering, **extra) -> dict:
    """Всё, что нужно шаблону; только JSON-типы — уходит в очередь Celery."""
    return {
        "gathering_id": gathering.pk,
        "slug": gathering.slug,
        "title": gathering.title,
        "place": gathering.place_name,
        "starts_at": gathering.starts_at.isoformat(),
        **extra,
    }


def _enabled_user_ids(user_ids, ntype) -> list[int]:
    if ntype in ALWAYS_ON:
        return list(user_ids)
    # Нет строки настроек — значит всё включено по умолчанию
    disabled = set(
        NotificationSettings.objects.filter(user_id__in=user_ids, **{ntype: False}).values_list(
            "user_id", flat=True
        )
    )
    return [uid for uid in user_ids if uid not in disabled]


def _throttled(user_id: int, gathering_id: int) -> bool:
    """True — уже уведомляли о чате недавно. cache.add атомарен: второй вызов вернёт False."""
    minutes = settings.KUN["CHAT_NOTIFY_THROTTLE_MINUTES"]
    return not cache.add(f"notify:chat:{gathering_id}:{user_id}", 1, timeout=minutes * 60)


def notify(user_ids, ntype: str, context: dict, *, sms: bool = False) -> None:
    """Поставить уведомление в очередь. sms=True — дополнительно SMS (отмена < 3 ч)."""
    from .tasks import deliver

    recipients = _enabled_user_ids(set(user_ids), ntype)
    if ntype == T.CHAT_MESSAGE:
        recipients = [u for u in recipients if not _throttled(u, context["gathering_id"])]

    for user_id in recipients:
        transaction.on_commit(lambda uid=user_id: deliver.delay(uid, str(ntype), context, sms=sms))
