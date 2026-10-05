"""Правила сборов. Всё, что меняет участников, — в transaction.atomic + select_for_update."""


def create_gathering(user, data):
    """Проверки: лимит 3 активных, окно времени, места, место из поиска (place_external_id).
    Автопроверка текста -> moderation_status=pending."""
    raise NotImplementedError


def update_gathering(gathering, user, data):
    """PATCH: время, место, комментарий. Системное сообщение + уведомление участникам."""
    raise NotImplementedError


def cancel_gathering(gathering, user, reason: str):
    """Отмена создателем. SMS участникам, если до начала < 3 часов."""
    raise NotImplementedError


def join_gathering(gathering, user):
    """Одна транзакция: свободные места, блокировки с участниками."""
    raise NotImplementedError


def leave_gathering(gathering, user):
    """Выход. < 2 часов до начала снижает надёжность.
    Если выходит создатель — передача роли (правила из «User flows»)."""
    raise NotImplementedError


def mark_attendance(gathering, user):
    raise NotImplementedError


def submit_ratings(gathering, user, ratings):
    raise NotImplementedError
