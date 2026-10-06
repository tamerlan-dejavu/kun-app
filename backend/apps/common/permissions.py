from django.db.models import Q
from django.utils import timezone
from rest_framework.permissions import BasePermission

from apps.common.exceptions import KunError


def active_sanctions(user, kinds):
    """Действующие санкции: не сняты и не истекли (бан — бессрочный, ends_at NULL)."""
    from apps.moderation.models import UserSanction

    now = timezone.now()
    return UserSanction.objects.filter(user=user, kind__in=kinds, revoked_at__isnull=True).filter(
        Q(ends_at__isnull=True) | Q(ends_at__gt=now)
    )


class IsActiveUser(BasePermission):
    """Вошёл, не удалён, прошёл онбординг (18+, согласия) и не заблокирован.

    Онбординг не требуется от staff (команда входит через /admin).
    Пауза не закрывает чтение — действия запрещает ensure_can_act().
    """

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.deleted_at is not None:
            return False
        if user.onboarding_completed_at is None and not user.is_staff:
            raise KunError("onboarding_required", "Сначала заверши регистрацию", 403)
        if active_sanctions(user, ["ban"]).exists():
            raise KunError("account_banned", "Аккаунт заблокирован", 403)
        return True


def ensure_can_act(user):
    """Создавать сборы, присоединяться и писать нельзя на паузе."""
    pause = active_sanctions(user, ["pause"]).order_by("-ends_at").first()
    if pause:
        until = timezone.localtime(pause.ends_at).strftime("%d.%m %H:%M")
        raise KunError("account_paused", f"Аккаунт на паузе до {until}", 403)


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_moderator)


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.role == "admin")
