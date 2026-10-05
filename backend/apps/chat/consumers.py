"""WebSocket чата: /ws/gatherings/<id>/ — комната на сбор (раздел 6 ТЗ).

Подключиться может только активный участник. Сообщения отправляются через REST
(POST /gatherings/{id}/messages), а сюда приходят события:
message.new, participant.joined, participant.left, gathering.updated, gathering.cancelled.

Коды закрытия: 4401 — не вошёл, 4403 — не участник сбора.
"""

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from apps.gatherings.models import Participation

from .services import group_name

CLOSE_NOT_AUTHENTICATED = 4401
CLOSE_NOT_PARTICIPANT = 4403


@database_sync_to_async
def is_participant(user, gathering_id: int) -> bool:
    return Participation.objects.filter(
        gathering_id=gathering_id, user=user, left_at__isnull=True
    ).exists()


class GatheringConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get("user")
        self.gathering_id = int(self.scope["url_route"]["kwargs"]["gathering_id"])
        self.group = group_name(self.gathering_id)

        # Соединение сначала принимаем, потом закрываем с кодом — так клиент видит причину
        await self.accept()
        if not (self.user and self.user.is_authenticated):
            await self.close(code=CLOSE_NOT_AUTHENTICATED)
            return
        if not await is_participant(self.user, self.gathering_id):
            await self.close(code=CLOSE_NOT_PARTICIPANT)
            return
        await self.channel_layer.group_add(self.group, self.channel_name)

    async def disconnect(self, code):
        if hasattr(self, "group"):
            await self.channel_layer.group_discard(self.group, self.channel_name)

    async def receive_json(self, content, **kwargs):
        # Отправка — через REST. Здесь только ping для поддержания соединения.
        if content.get("type") == "ping":
            await self.send_json({"type": "pong"})

    async def kun_event(self, event):
        await self.send_json({"type": event["event"], "data": event["data"]})
        # Вышедшего участника отключаем от комнаты
        if event["event"] == "participant.left" and event["data"].get("user_id") == self.user.pk:
            await self.close(code=CLOSE_NOT_PARTICIPANT)
