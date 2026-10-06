from django.contrib.gis.geos import Point
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.pagination import StartsAtCursorPagination

from . import selectors, services
from .city import city_snapshot
from .models import Gathering
from .serializers import (
    CancelSerializer,
    CitySnapshotSerializer,
    FeedParamsSerializer,
    GatheringCreateSerializer,
    GatheringDetailSerializer,
    GatheringListSerializer,
    GatheringPublicSerializer,
    GatheringUpdateSerializer,
    MyGatheringsParamsSerializer,
    RatingsSerializer,
)

TAGS = ["gatherings"]


class FeedPagination(CursorPagination):
    """По времени начала, а с координатами — по расстоянию."""

    page_size = 20

    def get_ordering(self, request, queryset, view):
        return ("distance_m", "id") if view.point is not None else ("starts_at", "id")


def get_visible(request, pk) -> Gathering:
    qs = selectors.with_counts(selectors.visible_gatherings(request.user), request.user)
    return get_object_or_404(qs, pk=pk)


def detail_response(request, gathering, code=status.HTTP_200_OK):
    gathering = get_visible(request, gathering.pk)
    return Response(GatheringDetailSerializer(gathering, context={"request": request}).data, code)


class GatheringListCreateView(ListAPIView):
    """GET /gatherings — лента; POST /gatherings — создать сбор."""

    serializer_class = GatheringListSerializer
    pagination_class = FeedPagination
    point = None

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):  # генерация OpenAPI без пользователя
            return Gathering.objects.none()
        params = FeedParamsSerializer(data=self.request.query_params)
        params.is_valid(raise_exception=True)
        p = params.validated_data
        if "lat" in p:
            self.point = Point(p["lng"], p["lat"], srid=4326)
        return selectors.feed_queryset(
            self.request.user, date=p.get("date"), category=p.get("category"), point=self.point
        )

    @extend_schema(tags=TAGS, parameters=[FeedParamsSerializer], summary="Лента сборов")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=TAGS,
        summary="Создать сбор",
        request=GatheringCreateSerializer,
        responses={201: GatheringDetailSerializer},
    )
    def post(self, request):
        serializer = GatheringCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        gathering = services.create_gathering(request.user, serializer.validated_data)
        return detail_response(request, gathering, status.HTTP_201_CREATED)


class GatheringDetailView(APIView):
    """GET /gatherings/{id}; PATCH — только создатель."""

    @extend_schema(tags=TAGS, summary="Сбор целиком", responses=GatheringDetailSerializer)
    def get(self, request, pk):
        return detail_response(request, get_visible(request, pk))

    @extend_schema(
        tags=TAGS,
        summary="Изменить время, место, комментарий (создатель)",
        request=GatheringUpdateSerializer,
        responses=GatheringDetailSerializer,
    )
    def patch(self, request, pk):
        gathering = get_visible(request, pk)
        serializer = GatheringUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        services.update_gathering(gathering, request.user, serializer.validated_data)
        return detail_response(request, gathering)


class GatheringCancelView(APIView):
    @extend_schema(
        tags=TAGS,
        summary="Отменить с причиной (создатель)",
        request=CancelSerializer,
        responses=GatheringDetailSerializer,
    )
    def post(self, request, pk):
        gathering = get_visible(request, pk)
        serializer = CancelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.cancel_gathering(gathering, request.user, serializer.validated_data["reason"])
        return detail_response(request, gathering)


class GatheringJoinView(APIView):
    @extend_schema(
        tags=TAGS, summary="Присоединиться", request=None, responses=GatheringDetailSerializer
    )
    def post(self, request, pk):
        gathering = get_visible(request, pk)
        services.join_gathering(gathering, request.user)
        return detail_response(request, gathering)


class GatheringLeaveView(APIView):
    @extend_schema(tags=TAGS, summary="Выйти", request=None, responses=GatheringDetailSerializer)
    def post(self, request, pk):
        gathering = get_visible(request, pk)
        services.leave_gathering(gathering, request.user)
        return detail_response(request, gathering)


class AttendanceView(APIView):
    @extend_schema(
        tags=TAGS,
        summary="«Я пришёл» (участник, от начала до +12 ч)",
        request=None,
        responses={204: OpenApiResponse(description="Отмечено")},
    )
    def post(self, request, pk):
        services.mark_attendance(get_visible(request, pk), request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RatingsView(APIView):
    @extend_schema(
        tags=TAGS,
        summary="Оценить участников (участник, до +48 ч)",
        request=RatingsSerializer,
        responses={204: OpenApiResponse(description="Сохранено")},
    )
    def post(self, request, pk):
        gathering = get_visible(request, pk)
        serializer = RatingsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.submit_ratings(gathering, request.user, serializer.validated_data["ratings"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyGatheringsView(ListAPIView):
    """GET /me/gatherings?when=upcoming|past"""

    serializer_class = GatheringListSerializer
    pagination_class = StartsAtCursorPagination

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Gathering.objects.none()
        params = MyGatheringsParamsSerializer(data=self.request.query_params)
        params.is_valid(raise_exception=True)
        return selectors.my_gatherings(self.request.user, params.validated_data["when"])

    @extend_schema(tags=TAGS, parameters=[MyGatheringsParamsSerializer], summary="Мои сборы")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PublicGatheringView(APIView):
    """Без входа: для SSR страницы /g/<slug> и превью в мессенджерах."""

    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        tags=TAGS, summary="Сбор по ссылке без личных данных", responses=GatheringPublicSerializer
    )
    def get(self, request, slug):
        qs = selectors.with_counts(
            Gathering.objects.filter(moderation_status=Gathering.ModerationStatus.PUBLISHED)
        )
        gathering = get_object_or_404(qs, slug=slug)
        return Response(GatheringPublicSerializer(gathering).data)


class PublicCityView(APIView):
    """GET /public/city — витрина для главной: сегодня, люди (анонимно), места, точки карты."""

    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(tags=TAGS, summary="Город сегодня (без входа)", responses=CitySnapshotSerializer)
    def get(self, request):
        return Response(CitySnapshotSerializer(city_snapshot()).data)
