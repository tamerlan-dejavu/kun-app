import logging

from celery import shared_task
from django.conf import settings

logger = logging.getLogger("kun.moderation")

# Истёкшие паузы снимать задачей не нужно: права проверяют ends_at (common.permissions).


@shared_task
def alert_moderators(report_id: int) -> str:
    """Критичная жалоба -> сразу в Telegram-чат модераторов (раздел 3.7 ТЗ).
    Без настроенного чата — в лог. Личных данных в тексте нет: только ссылка на жалобу."""
    from apps.notifications.channels import telegram

    from .models import Report

    report = Report.objects.filter(pk=report_id).first()
    if report is None:
        return "missing"
    text = (
        f"🚨 Критичная жалоба #{report.pk}: {report.get_reason_display()} "
        f"({report.get_target_type_display().lower()})"
    )
    url = f"{settings.SITE_URL}/admin/moderation/report/{report.pk}/change/"
    chat = settings.TELEGRAM_MODERATORS_CHAT_ID
    if chat and telegram.is_configured() and telegram.send_message(chat, text, url):
        return "telegram"
    logger.warning("%s — %s", text, url)
    return "log"
