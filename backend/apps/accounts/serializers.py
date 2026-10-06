from rest_framework import serializers

from .models import User


class PhoneRequestSerializer(serializers.Serializer):
    phone = serializers.CharField()


class PhoneVerifySerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField(min_length=6, max_length=6)


class MeSerializer(serializers.ModelSerializer):
    """Свой профиль: телефон виден только самому пользователю.
    TODO: запись (онбординг: 18+, согласия, имя, вуз, интересы) — вместе с входом по телефону."""

    university = serializers.CharField(source="university.short_name", default=None)
    onboarding_completed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "phone",
            "name",
            "photo",
            "university",
            "role",
            "reliability",
            "happened_gatherings_count",
            "onboarding_completed",
        ]
        read_only_fields = fields

    def get_onboarding_completed(self, obj) -> bool:
        return obj.onboarding_completed_at is not None


class PublicUserSerializer(serializers.Serializer):
    """Публичный профиль: имя, фото, значок вуза, интересы, счётчик сборов, надёжность.
    Телефон и почта не отдаются."""
