import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import UserManager


def avatar_upload_to(instance, filename):
    # Имя не раскрывает исходный файл; формат после обработки — WebP (apps.common.images)
    return f"avatars/{uuid.uuid4().hex}.webp"


class User(AbstractBaseUser, PermissionsMixin):
    """Пользователь KUN. Вход по номеру телефона (раздел 3.2 ТЗ)."""

    class Role(models.TextChoices):
        USER = "user", "Пользователь"
        MODERATOR = "moderator", "Модератор"
        ADMIN = "admin", "Администратор"

    phone = models.CharField(
        "телефон", max_length=16, unique=True, db_comment="+7XXXXXXXXXX, идентификатор входа"
    )
    name = models.CharField("имя", max_length=50, blank=True)
    photo = models.ImageField("фото", upload_to=avatar_upload_to, blank=True)
    interests = models.ManyToManyField(
        "catalog.Interest", related_name="users", blank=True, verbose_name="интересы"
    )
    role = models.CharField("роль", max_length=16, choices=Role.choices, default=Role.USER)

    university = models.ForeignKey(
        "universities.University",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        verbose_name="вуз",
        db_comment="по желанию, без подтверждения; ничего не ограничивает",
    )

    # Онбординг и согласия
    adult_confirmed_at = models.DateTimeField("подтвердил 18+", null=True, blank=True)
    terms_accepted_at = models.DateTimeField(
        "согласие с правилами и обработкой данных", null=True, blank=True
    )
    onboarding_completed_at = models.DateTimeField("онбординг завершён", null=True, blank=True)

    # Счётчики профиля (пересчитываются сервисами, а не на лету)
    reliability = models.FloatField(
        "надёжность",
        null=True,
        blank=True,
        db_comment="0..1 по последним 10 сборам; NULL — пока нет истории. Формула: docs/adr/0001",
    )
    happened_gatherings_count = models.PositiveIntegerField(
        "состоявшихся сборов", default=0, db_comment="сборы, где пользователь отметил «Я пришёл»"
    )

    is_staff = models.BooleanField("доступ в админку", default=False)
    is_active = models.BooleanField("активен", default=True)
    date_joined = models.DateTimeField("зарегистрирован", default=timezone.now)
    deleted_at = models.DateTimeField(
        "удалён", null=True, blank=True, db_comment="мягкое удаление через DELETE /me"
    )

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        db_table_comment = "Пользователи KUN: вход по телефону, профиль"

    def __str__(self):
        return self.name or self.phone

    @property
    def is_moderator(self) -> bool:
        return self.role in (self.Role.MODERATOR, self.Role.ADMIN)


class AuthCode(models.Model):
    """Код входа из SMS: 6 цифр, 5 минут, 5 попыток (раздел 3.2 ТЗ)."""

    phone = models.CharField("телефон", max_length=16, db_index=True)
    code_hash = models.CharField(
        "хэш кода", max_length=128, db_comment="сам код не храним, только хэш"
    )
    expires_at = models.DateTimeField("действует до")
    attempts = models.PositiveSmallIntegerField(
        "неверных вводов", default=0, db_comment="5 неверных -> locked_until"
    )
    locked_until = models.DateTimeField("заблокирован до", null=True, blank=True)
    used_at = models.DateTimeField("использован", null=True, blank=True)
    ip = models.GenericIPAddressField("IP запроса", null=True, blank=True)
    created_at = models.DateTimeField("создан", auto_now_add=True)

    class Meta:
        verbose_name = "код входа"
        verbose_name_plural = "коды входа"
        db_table_comment = "Коды входа по SMS (хэши), попытки и блокировки"
        indexes = [models.Index(fields=["phone", "-created_at"], name="authcode_phone_recent")]

    def __str__(self):
        return f"{self.phone} @ {self.created_at:%Y-%m-%d %H:%M}"


class UserSession(models.Model):
    """Связь сессии Django с пользователем: «выйти везде», удаление аккаунта, список устройств.

    Сама сессия — в django_session; здесь только индекс по пользователю.
    На этапе 3 сюда же ляжут refresh-токены приложений.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sessions")
    session_key = models.CharField("ключ сессии", max_length=40, unique=True)
    user_agent = models.CharField("браузер/устройство", max_length=300, blank=True)
    ip = models.GenericIPAddressField("IP", null=True, blank=True)
    created_at = models.DateTimeField("создана", auto_now_add=True)
    last_seen_at = models.DateTimeField("последняя активность", auto_now=True)

    class Meta:
        verbose_name = "сессия"
        verbose_name_plural = "сессии"
        db_table_comment = (
            "Сессии пользователя (ключ из django_session) — для выхода со всех устройств"
        )

    def __str__(self):
        return f"{self.user} — {self.user_agent[:40]}"
