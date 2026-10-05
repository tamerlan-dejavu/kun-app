import pytest


@pytest.mark.django_db
def test_health(api_client):
    resp = api_client.get("/api/v1/health/")
    assert resp.status_code == 200
