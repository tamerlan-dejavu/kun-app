"""SMS только при отмене сбора менее чем за 3 часа (раздел 3.5 ТЗ)."""

from apps.accounts.sms import send_sms


def send(user, text: str) -> None:
    send_sms(user.phone, text)
