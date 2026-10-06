import pytest

from apps.catalog.models import Category

pytestmark = pytest.mark.django_db


def test_categories_active_only(client_for, user):
    Category.objects.filter(slug="cinema").update(is_active=False)
    slugs = [c["slug"] for c in client_for(user).get("/api/v1/catalog/categories").json()]
    assert "walk" in slugs and "cinema" not in slugs


def test_interests(client_for, user):
    assert len(client_for(user).get("/api/v1/catalog/interests").json()) == 18
