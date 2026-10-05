from celery import shared_task


@shared_task
def lift_expired_pauses():
    raise NotImplementedError


@shared_task
def alert_moderators(report_id: int):
    raise NotImplementedError
