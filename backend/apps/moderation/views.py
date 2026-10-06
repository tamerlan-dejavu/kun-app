from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common import ratelimit

from . import services
from .serializers import BlockCreateSerializer, ReportCreateSerializer, ReportSerializer

TAGS = ["safety"]


class ReportCreateView(APIView):
    """POST /reports — жалоба на пользователя, сбор или сообщение."""

    @extend_schema(
        tags=TAGS,
        summary="Пожаловаться",
        request=ReportCreateSerializer,
        responses={201: ReportSerializer},
    )
    def post(self, request):
        ratelimit.enforce(request, "report-create", ratelimit.REPORT_CREATE)
        serializer = ReportCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        report = services.create_report(request.user, **serializer.validated_data)
        return Response(ReportSerializer(report).data, status=status.HTTP_201_CREATED)


class BlockCreateView(APIView):
    """POST /blocks"""

    @extend_schema(
        tags=TAGS,
        summary="Заблокировать",
        request=BlockCreateSerializer,
        responses={204: OpenApiResponse(description="Заблокирован")},
    )
    def post(self, request):
        serializer = BlockCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.block_user(request.user, serializer.validated_data["user_id"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class BlockDeleteView(APIView):
    """DELETE /blocks/{userId}"""

    @extend_schema(
        tags=TAGS, summary="Разблокировать", responses={204: OpenApiResponse(description="Снято")}
    )
    def delete(self, request, user_id):
        services.unblock_user(request.user, user_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
