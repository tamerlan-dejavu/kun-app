from django.db import models


class University(models.Model):
    """Вуз: название, короткое имя для значка. Ведёт администратор."""

    # TODO: name, short_name, is_active


class UniversityDomain(models.Model):
    """Почтовый домен вуза, например narxoz.kz."""

    # TODO: university FK, domain unique


class StudentEmailCode(models.Model):
    """Код подтверждения вузовской почты."""

    # TODO: user FK, email, code_hash, expires_at, attempts
