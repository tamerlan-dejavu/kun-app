"""Действия модератора — всегда с причиной и записью в ModerationLog."""


def hide_message(message, actor, reason: str):
    raise NotImplementedError


def hide_gathering(gathering, actor, reason: str):
    raise NotImplementedError


def warn(user, actor, reason: str):
    raise NotImplementedError


def pause(user, actor, reason: str, days: int = 7):
    raise NotImplementedError


def ban(user, actor, reason: str):
    raise NotImplementedError


def create_report(reporter, target_type, target_id, reason, text=""):
    """Критичные жалобы сразу дублируются в Telegram-чат модераторов."""
    raise NotImplementedError


def block_user(blocker, blocked):
    raise NotImplementedError


def unblock_user(blocker, blocked_id):
    raise NotImplementedError
