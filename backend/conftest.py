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
