"""SMS-шлюз: backend выбирается настройкой SMS_BACKEND.

console — dev, текст пишется в лог (номер замаскирован); dummy — тесты, копит в outbox;
provider — казахстанский шлюз (не выбран, открытый вопрос ТЗ).
"""

from django.conf import settings

from . import console, dummy, provider

BACKENDS = {"console": console, "dummy": dummy, "provider": provider}


def send_sms(phone: str, text: str) -> None:
    BACKENDS[settings.SMS_BACKEND].send(phone, text)


def mask(phone: str) -> str:
    """+77011234567 -> +7701*****67: в логах номер целиком не появляется."""
    return phone[:5] + "*" * max(len(phone) - 7, 0) + phone[-2:]
