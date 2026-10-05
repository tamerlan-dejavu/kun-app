from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Пользователь KUN. Вход по номеру телефона.

    Поля (раздел 6 ТЗ):
        phone               — уникальный, идентификатор входа (+7XXXXXXXXXX)
        name, photo         — обязательны после онбординга
        interests           — M2M catalog.Interest, 3–5 шт.
        role                — user | moderator | admin
        university          — FK universities.University, необязательно
        student_email       — необязательно
        student_verified_at — дата подтверждения значка, повтор раз в 12 мес.
        adult_confirmed_at  — подтверждение 18+
        terms_accepted_at   — согласие с правилами и обработкой данных
        reliability         — рейтинг надёжности (см. gatherings/reliability.py)
        telegram_chat_id    — после привязки бота
        deleted_at          — мягкое удаление (DELETE /me)
    """

    phone = models.CharField(max_length=16, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "phone"

    # TODO: остальные поля


class AuthCode(models.Model):
    """Код входа из SMS: хэш кода, срок (5 мин), число попыток (5 -> блок на 15 мин)."""

    # TODO: phone, code_hash, expires_at, attempts, locked_until, created_at, ip
