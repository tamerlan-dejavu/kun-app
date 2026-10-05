"""Единый формат ошибок API: {"code": "...", "message": "человеческий текст на русском"}.

Ошибки валидации дополнительно несут "fields": {поле: [сообщения]}.
"""

from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.http import Http404
from rest_framework import exceptions, status


class KunError(exceptions.APIException):
    """Бизнес-ошибка с кодом. Пример: raise KunError("gathering_full", "Мест больше нет")."""

    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, code: str, message: str, status_code: int | None = None):
        super().__init__(detail=message, code=code)
        self.code = code
        self.message = message
        if status_code:
            self.status_code = status_code


# Сообщения стандартных ошибок DRF — на «ты», коротко
DEFAULT_MESSAGES = {
    exceptions.NotAuthenticated: ("not_authenticated", "Нужно войти"),
    exceptions.AuthenticationFailed: ("not_authenticated", "Нужно войти заново"),
    exceptions.PermissionDenied: ("forbidden", "Сюда нельзя"),
    exceptions.NotFound: ("not_found", "Не нашли такого"),
    exceptions.MethodNotAllowed: ("method_not_allowed", "Так нельзя"),
    exceptions.Throttled: ("too_many_requests", "Слишком часто, попробуй чуть позже"),
    exceptions.UnsupportedMediaType: ("unsupported_media_type", "Неподдерживаемый формат"),
    exceptions.ParseError: ("bad_request", "Не получилось разобрать запрос"),
}


def _first_message(detail) -> str:
    if isinstance(detail, dict):
        for value in detail.values():
            return _first_message(value)
    if isinstance(detail, list) and detail:
        return _first_message(detail[0])
    return str(detail)


def exception_handler(exc, context):
    # Импорт здесь, а не наверху: rest_framework.views при загрузке читает настройки DRF,
    # которые ссылаются на apps.common.permissions -> этот модуль (циклический импорт)
    from rest_framework.views import exception_handler as drf_exception_handler

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, DjangoPermissionDenied):
        exc = exceptions.PermissionDenied()

    response = drf_exception_handler(exc, context)
    if response is None:
        return None

    if isinstance(exc, KunError):
        response.data = {"code": exc.code, "message": exc.message}
    elif isinstance(exc, exceptions.ValidationError):
        response.data = {
            "code": "validation_error",
            "message": _first_message(exc.detail),
            "fields": exc.detail if isinstance(exc.detail, dict) else {},
        }
    else:
        code, message = DEFAULT_MESSAGES.get(type(exc), ("error", _first_message(exc.detail)))
        if str(exc.detail).startswith("CSRF Failed"):
            response.data = {"code": "csrf_failed", "message": "Обнови страницу и попробуй ещё раз"}
            return response
        # PermissionDenied с конкретным текстом (например, из has_object_permission) — сохраняем
        if isinstance(exc, exceptions.PermissionDenied) and str(exc.detail) != str(
            exceptions.PermissionDenied.default_detail
        ):
            message = str(exc.detail)
        response.data = {"code": code, "message": message}
    return response
