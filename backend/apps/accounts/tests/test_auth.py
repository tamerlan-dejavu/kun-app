import pytest


@pytest.mark.skip("TODO")
def test_code_expires_after_5_minutes(): ...


@pytest.mark.skip("TODO")
def test_lock_after_5_wrong_attempts(): ...


@pytest.mark.skip("TODO")
def test_sms_limit_3_per_hour_per_phone(): ...


@pytest.mark.skip("TODO")
def test_one_phone_one_account(): ...


@pytest.mark.django_db
def test_me_returns_own_profile(client_for, user):
    data = client_for(user).get("/api/v1/me").json()
    assert data["id"] == user.id and data["phone"] == user.phone
    assert data["onboarding_completed"] is True
