"""dev: SMS не отправляются, текст пишется в лог (номер замаскирован)."""

import logging

logger = logging.getLogger("kun.sms")


def send(phone: str, text: str) -> None:
    from . import mask

    logger.info("SMS %s: %s", mask(phone), text)
