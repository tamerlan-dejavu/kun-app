from rest_framework import serializers


class PhoneRequestSerializer(serializers.Serializer):
    phone = serializers.CharField()


class PhoneVerifySerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField(min_length=6, max_length=6)


class MeSerializer(serializers.Serializer):
    """Свой профиль (с телефоном) + онбординг. TODO: ModelSerializer."""


class PublicUserSerializer(serializers.Serializer):
    """Публичный профиль: имя, фото, значок вуза, интересы, счётчик сборов, надёжность.
    Телефон и почта не отдаются."""
