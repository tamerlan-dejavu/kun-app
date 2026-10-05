"""Чат сбора (раздел 3.4 ТЗ): отправка, системные сообщения, рассылка по WebSocket.

Рассылка — только после коммита транзакции: клиент не получит сообщение, которого нет в БД.
TODO: уведомление участникам о новом сообщении (не чаще 1 раза в 10 минут) — с notifications.
"""

from datetime import timedelta

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.db import transaction
from django.utils import timezone

from apps.common.exceptions import KunError
from apps.common.permissions import ensure_can_act

from .models import Message

RULES = settings.KUN

# Системное событие в чате -> событие WebSocket из ТЗ (раздел 6)
SYSTEM_EVENT_TO_WS = {
    Message.SystemEvent.JOINED: "participant.joined",
    Message.SystemEvent.LEFT: "participant.left",
    Message.SystemEvent.UPDATED: "gathering.updated",
    Message.SystemEvent.CREATOR_CHANGED: "gathering.updated",
    Message.SystemEvent.CANCELLED: "gathering.cancelled",
}


def group_name(gathering_id: int) -> str:
    return f"gathering_{gathering_id}"


def broadcast(gathering_id: int, event: str, data: dict) -> None:
    """Событие всем подключённым участникам сбора: message.new, participant.joined,
    participant.left, gathering.updated, gathering.cancelled."""

    def send():
        layer = get_channel_layer()
        if layer is not None:
            async_to_sync(layer.group_send)(
                group_name(gathering_id), {"type": "kun.event", "event": event, "data": data}
            )

    transaction.on_commit(send)


def serialize(message: Message) -> dict:
    from .serializers import MessageSerializer

    return MessageSerializer(message).data


def is_read_only(gathering) -> bool:
    """Через 24 часа после начала чат только для чтения."""
    return timezone.now() > gathering.starts_at + timedelta(
        hours=RULES["CHAT_READONLY_AFTER_HOURS"]
    )


@transaction.atomic
def post_message(gathering, user, text: str) -> Message:
    """Только активный участник, не на паузе, чат не закрыт."""
    from apps.gatherings.models import Participation

    if not Participation.objects.filter(
        gathering=gathering, user=user, left_at__isnull=True
    ).exists():
        raise KunError("not_participant", "Писать в чат могут только участники сбора", 403)
    ensure_can_act(user)
    if is_read_only(gathering):
        raise KunError("chat_read_only", "Чат закрыт: прошло больше суток после встречи")

    text = text.strip()
    if not text:
        raise KunError("empty_message", "Сообщение пустое")

    message = Message.objects.create(gathering=gathering, author=user, text=text)
    broadcast(gathering.pk, "message.new", serialize(message))
    return message


def post_system_message(gathering, event: str, payload: dict | None = None) -> Message:
    """Системное сообщение: joined, left, updated, cancelled, creator_changed.
    Рассылается как message.new и как событие сбора (participant.joined и т. д.)."""
    message = Message.objects.create(
        gathering=gathering, kind=Message.Kind.SYSTEM, system_event=event, payload=payload or {}
    )
    broadcast(gathering.pk, "message.new", serialize(message))
    ws_event = SYSTEM_EVENT_TO_WS.get(event)
    if ws_event:
        broadcast(gathering.pk, ws_event, {"gathering_id": gathering.pk, **(payload or {})})
    return message
