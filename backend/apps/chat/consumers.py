from channels.generic.websocket import AsyncJsonWebsocketConsumer


class GatheringConsumer(AsyncJsonWebsocketConsumer):
    """/ws/gatherings/<id>/ — комната на сбор. Подключиться может только участник."""

    async def connect(self):
        # TODO: проверить участие, group_add, accept
        await self.close()

    async def disconnect(self, code):
        pass

    async def receive_json(self, content, **kwargs):
        # Отправка сообщений — через REST POST /gatherings/{id}/messages
        pass

    async def kun_event(self, event):
        await self.send_json({"type": event["event"], "data": event["data"]})
