from django.contrib.auth.backends import ModelBackend


class PhoneBackend(ModelBackend):
    """Аутентификация по телефону и коду из SMS; пароль — только для staff в /admin."""

    # TODO
