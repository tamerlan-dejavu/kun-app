"""Rate limit (раздел 4 ТЗ): SMS, вход, создание сборов, сообщения, жалобы.

Счётчики — в Redis через django-ratelimit. Превышение -> 429 {code: too_many_requests}.
"""

from django_ratelimit.core import is_ratelimited

from apps.common.exceptions import KunError

SMS_PER_PHONE = "3/h"
SMS_PER_IP = "10/d"
GATHERING_CREATE = "10/d"
CHAT_MESSAGE = "30/m"
REPORT_CREATE = "20/d"


def enforce(request, group: str, rate: str, key: str = "user") -> None:
    """Считает запрос и бросает 429, если лимит превышен. key — как в django-ratelimit."""
    if is_ratelimited(
        request, group=group, key=key, rate=rate, method=request.method, increment=True
    ):
        raise KunError("too_many_requests", "Слишком часто, попробуй чуть позже", 429)


def phone_key(group, request):
    """Ключ лимита по номеру телефона из тела запроса."""
    # TODO: нормализовать номер и вернуть его хэш (сам номер не храним в ключе)
    raise NotImplementedError
