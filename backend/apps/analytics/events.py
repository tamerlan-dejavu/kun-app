"""Серверные события в PostHog. Полный план — вкладка «Аналитика» документов MVP.

attendance_marked хранится с категорией и временем — основа персонального подбора (этап 2).
"""

ATTENDANCE_MARKED = "attendance_marked"
GATHERING_CREATED = "gathering_created"
GATHERING_JOINED = "gathering_joined"
GATHERING_LEFT = "gathering_left"
GATHERING_CANCELLED = "gathering_cancelled"
GATHERING_HAPPENED = "gathering_happened"  # >= 2 участника отметили «Я пришёл»
USER_SIGNED_UP = "user_signed_up"
ONBOARDING_COMPLETED = "onboarding_completed"


def capture(user, event: str, properties: dict | None = None) -> None:
    raise NotImplementedError
