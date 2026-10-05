from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MeSerializer


class PhoneRequestView(APIView):
    """POST /auth/phone/request — отправить код по SMS. Доступ: все."""

    permission_classes = [AllowAny]

    def post(self, request):
        raise NotImplementedError


class PhoneVerifyView(APIView):
    """POST /auth/phone/verify — проверить код, создать сессию. Доступ: все."""

    permission_classes = [AllowAny]

    def post(self, request):
        raise NotImplementedError


class LogoutView(APIView):
    """POST /auth/logout."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        raise NotImplementedError


class MeView(APIView):
    """GET /me, PATCH /me (онбординг), DELETE /me (удаление аккаунта)."""

    permission_classes = [IsAuthenticated]  # онбординг доступен до его завершения

    @extend_schema(tags=["me"], summary="Свой профиль", responses=MeSerializer)
    def get(self, request):
        return Response(MeSerializer(request.user).data)

    def patch(self, request):
        raise NotImplementedError

    def delete(self, request):
        raise NotImplementedError


class MePhotoView(APIView):
    """POST /me/photo — до 5 МБ, JPG/PNG/WebP."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        raise NotImplementedError


class UserDetailView(APIView):
    """GET /users/{id} — публичный профиль."""

    def get(self, request, pk):
        raise NotImplementedError
