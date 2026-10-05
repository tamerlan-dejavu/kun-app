"""SMS-шлюз: backend выбирается настройкой SMS_BACKEND (console | dummy | <провайдер РК>)."""


def send_sms(phone: str, text: str) -> None:
    raise NotImplementedError
