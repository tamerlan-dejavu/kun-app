from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response

from apps.common import ratelimit
from apps.common.exceptions import KunError
from apps.gatherings.models import Participation
from apps.gatherings.selectors import visible_gatherings

from . import services
from .models import Message
from .serializers import MessageCreateSerializer, MessageSerializer

TAGS = ["chat"]


class HistoryPagination(CursorPagination):
    """Новые сверху; клиент листает назад по курсору."""

    page_size = 50
    ordering = ("-created_at", "-id")


class MessageListCreateView(ListAPIView):
    """GET /gatherings/{id}/messages — история; POST — отправка. Только участник."""

    serializer_class = MessageSerializer
    pagination_class = HistoryPagination

    def get_gathering(self):
        gathering = get_object_or_404(visible_gatherings(self.request.user), pk=self.kwargs["pk"])
        is_member = Participation.objects.filter(
            gathering=gathering, user=self.request.user, left_at__isnull=True
        ).exists()
        if not is_member:
            raise KunError("not_participant", "Чат доступен только участникам сбора", 403)
        return gathering

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Message.objects.none()
        gathering = self.get_gathering()
        return Message.objects.filter(gathering=gathering).select_related("author__university")

    @extend_schema(tags=TAGS, summary="История чата (новые сверху)")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=TAGS,
        summary="Отправить сообщение",
        request=MessageCreateSerializer,
        responses={201: MessageSerializer},
    )
    def post(self, request, pk):
        gathering = self.get_gathering()
        ratelimit.enforce(request, "chat-message", ratelimit.CHAT_MESSAGE)
        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = services.post_message(gathering, request.user, serializer.validated_data["text"])
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
