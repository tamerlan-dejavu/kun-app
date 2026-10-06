"""Тесты: SMS складываются в outbox, как mail.outbox у Django."""

outbox: list[tuple[str, str]] = []


def send(phone: str, text: str) -> None:
    outbox.append((phone, text))
