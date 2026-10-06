"""Общие фикстуры pytest."""

import pytest
from django.core.cache import cache
from rest_framework.test import APIClient

from tests.factories import UserFactory


@pytest.fixture(autouse=True)
def clear_cache():
    """Каждый тест — с чистым кэшем: счётчики rate limit не переживают тест."""
    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.fixture
def client_for():
    """client_for(user) -> APIClient, вошедший как user."""

    def make(user):
        client = APIClient()
        client.force_authenticate(user)
        return client

    return make


@pytest.fixture
def sent_notifications(monkeypatch):
    """Перехватывает постановку уведомлений в очередь: список (user_id, type, context, sms).
    on_commit в диспетчере выполняется сразу — как будто транзакция уже закоммичена."""
    from apps.notifications import dispatcher, tasks

    calls = []
    monkeypatch.setattr(dispatcher.transaction, "on_commit", lambda fn: fn())
    monkeypatch.setattr(
        tasks.deliver,
        "delay",
        lambda uid, ntype, ctx, sms=False: calls.append((uid, ntype, ctx, sms)),
    )
    return calls
