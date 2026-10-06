from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.moderation.models import Block

from . import services
from .models import User
from .serializers import (
    MeSerializer,
    MeUpdateSerializer,
    PhotoUploadSerializer,
    PublicUserSerializer,
)

TAGS = ["me"]


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


def me_response(request):
    user = (
        User.objects.select_related("university")
        .prefetch_related("interests")
        .get(pk=request.user.pk)
    )
    return Response(MeSerializer(user, context={"request": request}).data)


class MeView(APIView):
    """GET /me, PATCH /me — профиль; DELETE /me — удаление аккаунта (TODO)."""

    permission_classes = [IsAuthenticated]  # онбординг доступен до его завершения

    @extend_schema(tags=TAGS, summary="Свой профиль", responses=MeSerializer)
    def get(self, request):
        return me_response(request)

    @extend_schema(
        tags=TAGS,
        summary="Изменить профиль: имя, вуз, интересы",
        request=MeUpdateSerializer,
        responses=MeSerializer,
    )
    def patch(self, request):
        serializer = MeUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        services.update_profile(request.user, serializer.validated_data)
        return me_response(request)

    def delete(self, request):
        raise NotImplementedError


class MePhotoView(APIView):
    """POST /me/photo — до 5 МБ, JPG/PNG/WebP; сервер обрезает до квадрата и убирает EXIF."""

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    @extend_schema(
        tags=TAGS, summary="Загрузить фото", request=PhotoUploadSerializer, responses=MeSerializer
    )
    def post(self, request):
        serializer = PhotoUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.set_photo(request.user, serializer.validated_data["photo"])
        return me_response(request)


class UserDetailView(APIView):
    """GET /users/{id} — публичный профиль. Кто заблокировал меня — для меня не существует."""

    @extend_schema(tags=["users"], summary="Профиль пользователя", responses=PublicUserSerializer)
    def get(self, request, pk):
        hidden = Block.objects.filter(blocker_id=pk, blocked=request.user).values("blocker_id")
        user = get_object_or_404(
            User.objects.filter(deleted_at__isnull=True, is_active=True)
            .exclude(pk__in=hidden)
            .select_related("university")
            .prefetch_related("interests"),
            pk=pk,
        )
        return Response(PublicUserSerializer(user, context={"request": request}).data)
