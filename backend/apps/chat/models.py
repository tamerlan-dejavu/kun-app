from django.db import models


class Message(models.Model):
    """Сообщение в чате сбора: до 1000 символов, только текст.

    kind: user | system (joined, left, updated); is_hidden — скрыто модератором.
    """

    # TODO: gathering FK, author FK null (для system), kind, text, payload JSON,
    #       is_hidden, created_at
