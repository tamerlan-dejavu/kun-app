"""Казахстанский SMS-шлюз. Провайдер не выбран — открытый вопрос ТЗ."""


def send(phone: str, text: str) -> None:
    raise NotImplementedError("SMS-провайдер ещё не выбран: SMS_BACKEND=console для dev")
