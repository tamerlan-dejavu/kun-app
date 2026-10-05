from celery import shared_task


@shared_task
def deliver(user_id: int, ntype: str, context: dict):
    raise NotImplementedError
