from django.db import models


class Report(models.Model):
    """Жалоба на пользователя, сбор или сообщение. Приоритет и сроки — вкладка «Безопасность»."""

    # TODO: reporter, target_type (user|gathering|message), target_id, reason, text,
    #       priority (critical|high|normal), status (new|in_review|resolved|rejected),
    #       assigned_to, resolved_at


class Block(models.Model):
    """Пользовательская блокировка: blocker -> blocked.
    Не видят сборы друг друга, не попадают в один сбор."""

    # TODO: blocker, blocked, created_at, unique


class UserSanction(models.Model):
    """Санкция модератора: warning | pause (7 дней) | ban."""

    # TODO: user, kind, reason, until, created_by, created_at


class BannedWord(models.Model):
    """Список запрещённых слов для автопроверки названия и комментария сбора."""

    # TODO: word, is_active


class ModerationLog(models.Model):
    """Неизменяемый журнал действий модераторов: кто, что, причина, когда.
    Запрет update/delete на уровне модели и admin."""

    # TODO: actor, action, target_type, target_id, reason, created_at
