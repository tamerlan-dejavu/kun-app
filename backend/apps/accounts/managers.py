from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """Обычные пользователи создаются при первом входе по коду (без пароля).
    Пароль есть только у staff — для входа в /admin."""

    use_in_migrations = True

    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("phone обязателен")
        user = self.model(phone=phone, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(phone, password, **extra_fields)
