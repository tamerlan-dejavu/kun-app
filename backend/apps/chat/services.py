def post_message(gathering, user, text: str):
    """Проверки: участник, чат не read-only (24 ч после начала), лимит.
    Рассылка в группу Channels."""
    raise NotImplementedError


def post_system_message(gathering, event: str, payload: dict | None = None):
    """Системное сообщение в чат сбора: joined, left, updated, cancelled, creator_changed.
    TODO: broadcast в группу Channels вместе с реализацией чата."""
    from .models import Message

    return Message.objects.create(
        gathering=gathering, kind=Message.Kind.SYSTEM, system_event=event, payload=payload or {}
    )


def broadcast(gathering_id: int, event: str, data: dict):
    """События: message.new, participant.joined, participant.left,
    gathering.updated, gathering.cancelled."""
    raise NotImplementedError
