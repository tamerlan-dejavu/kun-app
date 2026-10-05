"""Ключи и лимиты rate limit (django-ratelimit): SMS, вход, создание сборов, сообщения, жалобы."""

SMS_PER_PHONE = "3/h"
SMS_PER_IP = "10/d"
GATHERING_CREATE = "10/d"
CHAT_MESSAGE = "30/m"
REPORT_CREATE = "20/d"


def phone_key(group, request):
    """Ключ лимита по номеру телефона из тела запроса."""
    # TODO: нормализовать номер и вернуть его хэш (сам номер не храним в ключе)
    raise NotImplementedError
