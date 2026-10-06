"""REST чата: история и отправка."""

from datetime import timedelta

import pytest
from django.utils import timezone

from apps.chat.models import Message
from apps.chat.serializers import HIDDEN_TEXT
from apps.gatherings.models import Gathering
from apps.moderation.models import UserSanction
from tests.factories import MessageFactory, ParticipationFactory, UserFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def member():
    """Участник сбора и URL чата."""
    p = ParticipationFactory()
    return p.user, f"/api/v1/gatherings/{p.gathering_id}/messages", p.gathering


def test_post_and_history(client_for, member):
    user, url, g = member
    client = client_for(user)
    r = client.post(url, {"text": "  Привет!  "}, format="json")
    assert r.status_code == 201
    assert r.json()["text"] == "Привет!"
    assert r.json()["author"]["id"] == user.id

    MessageFactory(gathering=g, author=None, kind="system", system_event="joined", text="")
    history = client.get(url).json()["results"]
    assert [m["kind"] for m in history] == ["system", "user"]  # новые сверху


def test_only_participant(client_for, member):
    _, url, _ = member
    client = client_for(UserFactory())
    assert client.get(url).json()["code"] == "not_participant"
    assert client.post(url, {"text": "x"}, format="json").status_code == 403


def test_left_participant_loses_access(client_for, member):
    user, url, g = member
    g.participations.filter(user=user).update(left_at=timezone.now())
    assert client_for(user).get(url).status_code == 403


def test_hidden_message_text_replaced(client_for, member):
    user, url, g = member
    MessageFactory(gathering=g, text="грубость", is_hidden=True)
    m = client_for(user).get(url).json()["results"][0]
    assert m["text"] == HIDDEN_TEXT and m["is_hidden"] is True


def test_read_only_after_24h(client_for, member):
    user, url, g = member
    Gathering.objects.filter(pk=g.pk).update(starts_at=timezone.now() - timedelta(hours=25))
    r = client_for(user).post(url, {"text": "Как добрались?"}, format="json")
    assert r.json()["code"] == "chat_read_only"


@pytest.mark.parametrize(
    "text, code", [("   ", "validation_error"), ("x" * 1001, "validation_error")]
)
def test_text_validation(client_for, member, text, code):
    user, url, _ = member
    assert client_for(user).post(url, {"text": text}, format="json").json()["code"] == code


def test_paused_cannot_write(client_for, member):
    user, url, _ = member
    UserSanction.objects.create(
        user=user,
        kind="pause",
        reason="x",
        ends_at=timezone.now() + timedelta(days=7),
        created_by=UserFactory(),
    )
    assert (
        client_for(user).post(url, {"text": "x"}, format="json").json()["code"] == "account_paused"
    )


def test_rate_limit(client_for, member):
    user, url, _ = member
    client = client_for(user)
    codes = [client.post(url, {"text": f"#{i}"}, format="json").status_code for i in range(31)]
    assert codes[:30] == [201] * 30
    assert codes[30] == 429
    assert Message.objects.filter(author=user).count() == 30


def test_join_and_leave_write_system_messages(client_for, member):
    _, url, g = member
    newcomer = UserFactory()
    client = client_for(newcomer)
    client.post(f"/api/v1/gatherings/{g.id}/join")
    client.post(f"/api/v1/gatherings/{g.id}/leave")
    events = list(
        Message.objects.filter(gathering=g, kind="system")
        .order_by("created_at", "id")
        .values_list("system_event", flat=True)
    )
    assert events == ["joined", "left"]
