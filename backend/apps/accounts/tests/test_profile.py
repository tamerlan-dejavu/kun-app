"""Профиль: свой (редактирование, фото) и чужой."""

import os
from io import BytesIO

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from apps.catalog.models import Interest
from apps.gatherings.models import Attendance
from apps.moderation.models import Block
from apps.universities.models import University
from tests.factories import GatheringFactory, UserFactory

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def media(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path


def image_file(fmt="JPEG", size=(1200, 800), name="me.jpg", with_gps=True):
    img = Image.new("RGB", size, "teal")
    buf = BytesIO()
    kwargs = {}
    if with_gps and fmt == "JPEG":
        exif = Image.Exif()
        exif[0x010F] = "PhoneMaker"
        exif[0x8825] = {1: "N", 2: (43.0, 14.0, 0.0)}  # GPSInfo — геометка
        kwargs["exif"] = exif.tobytes()
    img.save(buf, fmt, **kwargs)
    return SimpleUploadedFile(name, buf.getvalue(), content_type=f"image/{fmt.lower()}")


def upload(client, file):
    return client.post("/api/v1/me/photo", {"photo": file}, format="multipart")


def test_patch_profile(client_for, user):
    uni = University.objects.get(short_name="Narxoz")
    slugs = ["music", "books", "coffee"]
    r = client_for(user).patch(
        "/api/v1/me", {"name": "  Аружан ", "university": uni.id, "interests": slugs}, format="json"
    )
    assert r.status_code == 200, r.json()
    data = r.json()
    assert data["name"] == "Аружан" and data["university"] == "Narxoz"
    assert sorted(i["slug"] for i in data["interests"]) == sorted(slugs)


@pytest.mark.parametrize(
    "interests",
    [["music", "books"], ["music", "books", "coffee", "sport", "art", "photo"]],
)
def test_interests_3_to_5(client_for, user, interests):
    r = client_for(user).patch("/api/v1/me", {"interests": interests}, format="json")
    assert r.json()["code"] == "validation_error"
    assert "interests" in r.json()["fields"]


def test_university_can_be_cleared(client_for, user):
    r = client_for(user).patch("/api/v1/me", {"university": None}, format="json")
    assert r.json()["university"] is None


def test_source_image_really_has_gps():
    """Проверка самого теста: исходник действительно с EXIF и геометкой."""
    with Image.open(image_file()) as src:
        assert 0x8825 in src.getexif()


def test_photo_square_webp_without_exif(client_for, user):
    r = upload(client_for(user), image_file())
    assert r.status_code == 200, r.json()
    user.refresh_from_db()
    with Image.open(user.photo.path) as saved:
        assert saved.format == "WEBP"
        assert saved.size == (512, 512)
        assert not saved.getexif()  # геометка и прочий EXIF не сохранились
    assert user.photo.name.endswith(".webp")


def test_photo_replaces_old_file(client_for, user):
    client = client_for(user)
    upload(client, image_file())
    user.refresh_from_db()
    first = user.photo.path
    upload(client, image_file(fmt="PNG", name="b.png"))
    user.refresh_from_db()
    assert user.photo.path != first
    assert not os.path.exists(first)


def test_photo_rejects_garbage_gif_and_big(client_for, user, settings):
    client = client_for(user)
    junk = SimpleUploadedFile("x.jpg", b"not an image", content_type="image/jpeg")
    assert upload(client, junk).json()["code"] == "photo_invalid"
    gif = image_file(fmt="GIF", name="a.gif", with_gps=False)
    assert upload(client, gif).json()["code"] == "photo_format"
    settings.KUN = {**settings.KUN, "PHOTO_MAX_BYTES": 100}
    assert upload(client, image_file()).json()["code"] == "photo_too_large"


def test_public_profile(client_for, user):
    other = UserFactory(name="Тимур")
    music = Interest.objects.get(slug="music")
    user.interests.set([music, Interest.objects.get(slug="books")])
    other.interests.set([music, Interest.objects.get(slug="sport")])
    g = GatheringFactory()
    Attendance.objects.create(gathering=g, user=user)
    Attendance.objects.create(gathering=g, user=other)

    data = client_for(user).get(f"/api/v1/users/{other.id}").json()
    assert data["name"] == "Тимур"
    assert "phone" not in data
    assert data["common_interests"] == ["music"]
    assert data["together_count"] == 1
    assert data["is_blocked"] is False


def test_profile_hidden_from_blocked(client_for, user):
    other = UserFactory()
    Block.objects.create(blocker=other, blocked=user)  # other заблокировал user
    assert client_for(user).get(f"/api/v1/users/{other.id}").status_code == 404
    # а other видит user и может снять блокировку
    assert client_for(other).get(f"/api/v1/users/{user.id}").json()["is_blocked"] is True


def test_deleted_user_404(client_for, user):
    from django.utils import timezone

    gone = UserFactory(deleted_at=timezone.now())
    assert client_for(user).get(f"/api/v1/users/{gone.id}").status_code == 404


def test_universities_catalog(client_for, user):
    names = [u["short_name"] for u in client_for(user).get("/api/v1/catalog/universities").json()]
    assert "Narxoz" in names
