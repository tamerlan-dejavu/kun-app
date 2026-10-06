"""Профиль: редактирование, фото. TODO: онбординг и удаление — вместе с входом по телефону."""

from django.db import transaction

from apps.common.images import process_avatar


def complete_onboarding(user, *, name, interests, adult_confirmed, terms_accepted):
    raise NotImplementedError


@transaction.atomic
def update_profile(user, data: dict):
    """name, university (или None), interests — уже проверены сериализатором."""
    fields = []
    if "name" in data:
        user.name = data["name"]
        fields.append("name")
    if "university" in data:
        user.university = data["university"]
        fields.append("university")
    if fields:
        user.save(update_fields=fields)
    if "interests" in data:
        user.interests.set(data["interests"])
    return user


def set_photo(user, uploaded_file):
    """Обработать и сохранить фото; старый файл удаляем, чтобы не копить мусор в хранилище."""
    content = process_avatar(uploaded_file)
    old = user.photo.name if user.photo else None
    user.photo.save(content.name, content, save=True)
    if old and old != user.photo.name:
        user.photo.storage.delete(old)
    return user


def delete_account(user):
    """Мягкое удаление: обезличить профиль, выйти из будущих сборов, передать роль создателя."""
    raise NotImplementedError
