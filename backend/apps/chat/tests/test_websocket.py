"""WebSocket чата через тестовый клиент Channels (раздел 9 ТЗ)."""

import pytest
from channels.db import database_sync_to_async
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.contrib.auth.models import AnonymousUser

from apps.chat import services
from apps.chat.consumers import CLOSE_NOT_AUTHENTICATED, CLOSE_NOT_PARTICIPANT
from apps.chat.routing import websocket_urlpatterns
from apps.gatherings import services as gathering_services
from tests.factories import ParticipationFactory, UserFactory

pytestmark = [pytest.mark.asyncio, pytest.mark.django_db(transaction=True)]

app = URLRouter(websocket_urlpatterns)


def communicator(gathering_id, user):
    c = WebsocketCommunicator(app, f"/ws/gatherings/{gathering_id}/")
    c.scope["user"] = user  # в проде это делает AuthMiddlewareStack по сессионной куке
    return c


@database_sync_to_async
def member():
    p = ParticipationFactory()
    return p.user, p.gathering


async def expect_close(c, code):
    connected, _ = await c.connect()
    assert connected  # принимаем, затем закрываем с кодом причины
    assert await c.receive_output() == {"type": "websocket.close", "code": code}


async def test_anonymous_rejected():
    _, g = await member()
    await expect_close(communicator(g.id, AnonymousUser()), CLOSE_NOT_AUTHENTICATED)


async def test_non_participant_rejected():
    _, g = await member()
    stranger = await database_sync_to_async(UserFactory)()
    await expect_close(communicator(g.id, stranger), CLOSE_NOT_PARTICIPANT)


async def test_participant_receives_new_message():
    user, g = await member()
    c = communicator(g.id, user)
    connected, _ = await c.connect()
    assert connected

    await database_sync_to_async(services.post_message)(g, user, "Я на месте")
    event = await c.receive_json_from(timeout=2)
    assert event["type"] == "message.new"
    assert event["data"]["text"] == "Я на месте"

    await c.send_json_to({"type": "ping"})
    assert await c.receive_json_from() == {"type": "pong"}
    await c.disconnect()


async def test_join_broadcasts_and_leave_disconnects():
    user, g = await member()
    c = communicator(g.id, user)
    await c.connect()

    newcomer = await database_sync_to_async(UserFactory)()
    await database_sync_to_async(gathering_services.join_gathering)(g, newcomer)
    types = {(await c.receive_json_from(timeout=2))["type"] for _ in range(2)}
    assert types == {"message.new", "participant.joined"}

    # Сам участник выходит — получает событие и отключается от комнаты
    await database_sync_to_async(gathering_services.leave_gathering)(g, user)
    received = [(await c.receive_json_from(timeout=2))["type"] for _ in range(2)]
    assert "participant.left" in received
    assert await c.receive_output(timeout=2) == {"type": "websocket.close", "code": 4403}
