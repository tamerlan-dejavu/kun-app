from celery import shared_task


@shared_task
def send_reminders():
    """Напоминание всем участникам за 2 часа до начала."""
    raise NotImplementedError


@shared_task
def finish_gatherings():
    """Перевод начавшихся сборов в finished; чат — только чтение через 24 часа."""
    raise NotImplementedError


@shared_task
def send_after_prompts():
    """«Как прошла встреча?» через 1 час после начала."""
    raise NotImplementedError
