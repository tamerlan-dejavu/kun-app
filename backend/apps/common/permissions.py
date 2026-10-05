from rest_framework.permissions import BasePermission


class IsActiveUser(BasePermission):
    """Вошёл, прошёл онбординг (18+, согласия), не заблокирован и не на паузе."""

    def has_permission(self, request, view):
        # TODO: проверить onboarding_completed_at, deleted_at, активные санкции
        return bool(request.user and request.user.is_authenticated)


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        # TODO: role in (moderator, admin)
        return False


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        # TODO: role == admin
        return False
