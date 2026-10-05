"""Web Push через pywebpush (на iPhone — только PWA, добавленная на главный экран)."""

import json
import logging

from django.conf import settings
from django.utils import timezone
from pywebpush import WebPushException, webpush

logger = logging.getLogger(__name__)
GONE = {404, 410}  # подписка больше не существует — удаляем


def is_configured() -> bool:
    return bool(settings.VAPID_PRIVATE_KEY)


def send(subscription, payload: dict) -> bool:
    try:
        webpush(
            subscription_info={"endpoint": subscription.endpoint, "keys": subscription.keys},
            data=json.dumps(payload, ensure_ascii=False),
            vapid_private_key=settings.VAPID_PRIVATE_KEY,
            vapid_claims={"sub": settings.VAPID_SUBJECT},
            timeout=5,
        )
    except WebPushException as e:
        status = getattr(e.response, "status_code", None)
        if status in GONE:
            subscription.delete()
        else:
            logger.warning("webpush: не доставлено (status=%s)", status)
        return False
    subscription.last_used_at = timezone.now()
    subscription.save(update_fields=["last_used_at"])
    return True
