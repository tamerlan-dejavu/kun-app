def post_message(gathering, user, text: str):
    """Проверки: участник, чат не read-only (24 ч после начала), лимит.
    Рассылка в группу Channels."""
    raise NotImplementedError


def post_system_message(gathering, event: str, payload: dict):
    raise NotImplementedError


def broadcast(gathering_id: int, event: str, data: dict):
    """События: message.new, participant.joined, participant.left,
    gathering.updated, gathering.cancelled."""
    raise NotImplementedError
