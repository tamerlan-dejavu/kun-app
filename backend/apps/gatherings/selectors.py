"""Запросы на чтение: лента, мои сборы."""


def feed_queryset(user, *, date=None, category=None, students_only=False, point=None):
    """status=open, moderation_status=published, без заблокированных и создателей с санкциями;
    сортировка по starts_at или по расстоянию (если передан point)."""
    raise NotImplementedError


def my_gatherings(user):
    """Будущие и прошедшие."""
    raise NotImplementedError
