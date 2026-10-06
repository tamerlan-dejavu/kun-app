from celery import shared_task

# Истёкшие паузы снимать задачей не нужно: права проверяют ends_at (common.permissions).


@shared_task
def alert_moderators(report_id: int):
    """Критичная жалоба -> сразу в Telegram-чат модераторов.
    TODO: вместе с жалобами (POST /reports)."""
    raise NotImplementedError
