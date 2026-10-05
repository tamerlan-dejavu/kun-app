from celery import shared_task


@shared_task
def expire_student_badges():
    """Снять значок, если student_verified_at старше 12 месяцев, и напомнить пройти проверку."""
    raise NotImplementedError
