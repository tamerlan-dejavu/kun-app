from django.contrib.gis.geos import Point
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.accounts.models import User
from apps.catalog.models import Category

from .models import SEATS_MAX, SEATS_MIN, Gathering, Rating

# --- вложенные -------------------------------------------------------------------------------


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["slug", "name", "emoji"]


class UserShortSerializer(serializers.ModelSerializer):
    """Участник в сборе: имя, фото, вуз. Телефон не отдаём никогда."""

    university = serializers.CharField(source="university.short_name", default=None)

    class Meta:
        model = User
        fields = ["id", "name", "photo", "university"]


class ParticipantSerializer(serializers.Serializer):
    user = UserShortSerializer()
    is_creator = serializers.BooleanField()
    joined_at = serializers.DateTimeField()


# --- чтение ----------------------------------------------------------------------------------


class GatheringListSerializer(serializers.ModelSerializer):
    """Карточка ленты."""

    category = CategorySerializer()
    participants_count = serializers.IntegerField()
    is_participant = serializers.BooleanField(default=False)
    distance_m = serializers.FloatField(
        required=False, allow_null=True, help_text="если в запросе были lat/lng"
    )

    class Meta:
        model = Gathering
        fields = [
            "id",
            "slug",
            "title",
            "category",
            "starts_at",
            "place_name",
            "district",
            "seats",
            "participants_count",
            "status",
            "is_participant",
            "distance_m",
        ]
        # slug генерируется моделью: в ответе есть всегда (иначе в OpenAPI он «необязательный»)
        read_only_fields = ["slug"]


class GatheringDetailSerializer(GatheringListSerializer):
    """Сбор целиком: точный адрес, координаты, участники."""

    lat = serializers.SerializerMethodField()
    lng = serializers.SerializerMethodField()
    creator = UserShortSerializer()
    participants = serializers.SerializerMethodField()
    is_creator = serializers.SerializerMethodField()

    class Meta(GatheringListSerializer.Meta):
        fields = [
            *GatheringListSerializer.Meta.fields,
            "comment",
            "address",
            "place_external_id",
            "lat",
            "lng",
            "creator",
            "is_creator",
            "participants",
            "moderation_status",
            "cancel_reason",
            "cancelled_at",
            "created_at",
        ]

    @extend_schema_field(serializers.FloatField())
    def get_lat(self, obj):
        return obj.location.y

    @extend_schema_field(serializers.FloatField())
    def get_lng(self, obj):
        return obj.location.x

    @extend_schema_field(serializers.BooleanField())
    def get_is_creator(self, obj):
        request = self.context.get("request")
        return bool(request and obj.creator_id == request.user.pk)

    @extend_schema_field(ParticipantSerializer(many=True))
    def get_participants(self, obj):
        active = (
            obj.participations.filter(left_at__isnull=True)
            .select_related("user__university")
            .order_by("-is_creator", "joined_at")
        )
        return ParticipantSerializer(active, many=True, context=self.context).data


class GatheringPublicSerializer(serializers.ModelSerializer):
    """Для страницы /g/<slug> гостю и Open Graph: без имён, фото и точного адреса."""

    category = CategorySerializer()
    participants_count = serializers.IntegerField()

    class Meta:
        model = Gathering
        fields = [
            "id",  # нужен вошедшему для действий (join, чат); личных данных не раскрывает
            "slug",
            "title",
            "category",
            "starts_at",
            "district",
            "seats",
            "participants_count",
            "status",
        ]
        read_only_fields = ["slug"]


# --- запись ----------------------------------------------------------------------------------


class PlaceFieldsMixin(serializers.Serializer):
    """Место из поиска 2ГИС: координаты приходят отдельными полями, в БД — PointField."""

    lat = serializers.FloatField(min_value=-90, max_value=90, write_only=True)
    lng = serializers.FloatField(min_value=-180, max_value=180, write_only=True)

    def to_point(self, attrs):
        lat, lng = attrs.pop("lat", None), attrs.pop("lng", None)
        if lat is not None and lng is not None:
            attrs["location"] = Point(lng, lat, srid=4326)
        elif (lat is None) != (lng is None):
            raise serializers.ValidationError({"lat": "Нужны обе координаты: lat и lng"})
        return attrs


class GatheringCreateSerializer(PlaceFieldsMixin, serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.filter(is_active=True)
    )
    seats = serializers.IntegerField(min_value=SEATS_MIN, max_value=SEATS_MAX)

    class Meta:
        model = Gathering
        fields = [
            "category",
            "title",
            "comment",
            "place_name",
            "address",
            "district",
            "place_external_id",
            "lat",
            "lng",
            "starts_at",
            "seats",
        ]
        extra_kwargs = {"place_external_id": {"allow_blank": False}}

    def validate(self, attrs):
        return self.to_point(attrs)


class GatheringUpdateSerializer(PlaceFieldsMixin, serializers.ModelSerializer):
    """Изменить можно время, место, комментарий. Место меняется целиком."""

    lat = serializers.FloatField(min_value=-90, max_value=90, write_only=True, required=False)
    lng = serializers.FloatField(min_value=-180, max_value=180, write_only=True, required=False)

    class Meta:
        model = Gathering
        fields = [
            "starts_at",
            "comment",
            "place_name",
            "address",
            "district",
            "place_external_id",
            "lat",
            "lng",
        ]

    def validate(self, attrs):
        place = {"place_name", "address", "place_external_id", "lat", "lng"}
        given = place & attrs.keys()
        if given and given != place:
            raise serializers.ValidationError(
                "Место меняется целиком: place_name, address, place_external_id, lat, lng"
            )
        return self.to_point(attrs)


class CancelSerializer(serializers.Serializer):
    reason = serializers.CharField(max_length=300)


class RatingItemSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    value = serializers.ChoiceField(choices=Rating.Value.choices)


class RatingsSerializer(serializers.Serializer):
    ratings = RatingItemSerializer(many=True, allow_empty=False)


class FeedParamsSerializer(serializers.Serializer):
    """Параметры ленты."""

    date = serializers.ChoiceField(
        choices=["today", "tomorrow", "week"], required=False, help_text="по календарю Алматы"
    )
    category = serializers.SlugField(required=False, help_text="slug категории")
    lat = serializers.FloatField(min_value=-90, max_value=90, required=False)
    lng = serializers.FloatField(min_value=-180, max_value=180, required=False)

    def validate(self, attrs):
        if ("lat" in attrs) != ("lng" in attrs):
            raise serializers.ValidationError({"lat": "Нужны обе координаты: lat и lng"})
        return attrs


class MyGatheringsParamsSerializer(serializers.Serializer):
    when = serializers.ChoiceField(choices=["upcoming", "past"], default="upcoming")
