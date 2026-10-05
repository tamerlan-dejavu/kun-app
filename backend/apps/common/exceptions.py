"""Единый формат ошибок API: {"code": "...", "message": "человеческий текст на русском"}."""

from rest_framework.views import exception_handler as drf_exception_handler


class KunError(Exception):
    """Бизнес-ошибка с кодом. Пример: KunError("gathering_full", "Мест больше нет")."""

    status_code = 400

    def __init__(self, code: str, message: str, status_code: int | None = None):
        self.code = code
        self.message = message
        if status_code:
            self.status_code = status_code


def exception_handler(exc, context):
    # TODO: KunError -> {code, message}; ValidationError/NotAuthenticated/Throttled -> тот же формат
    return drf_exception_handler(exc, context)
