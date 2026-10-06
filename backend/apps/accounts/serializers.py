from rest_framework import serializers

from apps.catalog.models import Interest
from apps.catalog.serializers import InterestSerializer
from apps.universities.models import University

from .models import User


class PhoneRequestSerializer(serializers.Serializer):
    phone = serializers.CharField()


class PhoneVerifySerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField(min_length=6, max_length=6)


class MeSerializer(serializers.ModelSerializer):
    """Свой профиль: телефон виден только самому пользователю."""

    university = serializers.CharField(source="university.short_name", default=None)
    university_id = serializers.IntegerField(allow_null=True)
    interests = InterestSerializer(many=True)
    onboarding_completed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "phone",
            "name",
            "photo",
            "university",
            "university_id",
            "interests",
            "role",
            "reliability",
            "happened_gatherings_count",
            "date_joined",
            "onboarding_completed",
        ]
        read_only_fields = fields

    def get_onboarding_completed(self, obj) -> bool:
        return obj.onboarding_completed_at is not None


class MeUpdateSerializer(serializers.Serializer):
    """Редактирование профиля. Интересы — от 3 до 5 (раздел 3.2 ТЗ)."""

    name = serializers.CharField(min_length=1, max_length=50, trim_whitespace=True)
    university = serializers.PrimaryKeyRelatedField(
        queryset=University.objects.filter(is_active=True), allow_null=True
    )
    interests = serializers.SlugRelatedField(
        slug_field="slug", queryset=Interest.objects.filter(is_active=True), many=True
    )

    def validate_interests(self, value):
        if not 3 <= len(value) <= 5:
            raise serializers.ValidationError("Выбери от 3 до 5 интересов")
        return value


class PhotoUploadSerializer(serializers.Serializer):
    photo = serializers.FileField()


class PublicUserSerializer(serializers.ModelSerializer):
    """Чужой профиль: имя, фото, вуз, интересы, сборы, надёжность. Телефона нет."""

    university = serializers.CharField(source="university.short_name", default=None)
    interests = InterestSerializer(many=True)
    common_interests = serializers.SerializerMethodField(help_text="slug общих интересов со мной")
    together_count = serializers.SerializerMethodField(
        help_text="на скольких сборах мы оба отметили «Я пришёл»"
    )
    is_blocked = serializers.SerializerMethodField(help_text="я заблокировал этого человека")

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "photo",
            "university",
            "interests",
            "happened_gatherings_count",
            "reliability",
            "date_joined",
            "common_interests",
            "together_count",
            "is_blocked",
        ]
        read_only_fields = fields

    def _me(self):
        return self.context["request"].user

    def get_common_interests(self, obj) -> list[str]:
        mine = set(self._me().interests.values_list("slug", flat=True))
        return [i.slug for i in obj.interests.all() if i.slug in mine]

    def get_together_count(self, obj) -> int:
        from apps.gatherings.models import Attendance

        me = self._me()
        if me.pk == obj.pk:
            return 0
        return Attendance.objects.filter(user=me, gathering__attendances__user=obj).count()

    def get_is_blocked(self, obj) -> bool:
        from apps.moderation.models import Block

        return Block.objects.filter(blocker=self._me(), blocked=obj).exists()
