"""Общие фикстуры pytest: api_client, user, другие фабрики — см. tests/factories.py."""

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()
