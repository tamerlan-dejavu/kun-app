"""Онбординг, профиль, удаление аккаунта."""


def complete_onboarding(user, *, name, interests, adult_confirmed, terms_accepted):
    raise NotImplementedError


def set_photo(user, uploaded_file):
    """Через apps.common.images.process_avatar."""
    raise NotImplementedError


def delete_account(user):
    """Мягкое удаление: обезличить профиль, выйти из будущих сборов, передать роль создателя."""
    raise NotImplementedError
