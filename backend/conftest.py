"""Общие фикстуры pytest."""

import pytest
from rest_framework.test import APIClient

from tests.factories import UserFactory


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
