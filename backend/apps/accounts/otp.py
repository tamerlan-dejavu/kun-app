"""Коды входа: генерация, хэш, проверка, лимиты (раздел 3.2 ТЗ).

- 6 цифр, действует 5 минут
- 3 отправки на номер в час, 10 в сутки с одного IP
- 5 неверных вводов -> блокировка на 15 минут
"""


def request_code(phone: str, ip: str) -> None:
    raise NotImplementedError


def verify_code(phone: str, code: str):
    """Возвращает User (создаёт при первом входе) или бросает KunError."""
    raise NotImplementedError
