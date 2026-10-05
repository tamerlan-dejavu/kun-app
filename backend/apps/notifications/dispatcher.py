"""Выбор каналов с учётом настроек и троттлинга; сама отправка — в Celery."""


def notify(users, ntype, context: dict) -> None:
    raise NotImplementedError
