from rest_framework import serializers

from apps.gatherings.serializers import UserShortSerializer

from .models import MESSAGE_MAX_LENGTH, Message

HIDDEN_TEXT = "Сообщение скрыто модератором"


class MessageSerializer(serializers.ModelSerializer):
    """Сообщение в истории и в событии message.new. Скрытое — без текста и данных."""

    author = UserShortSerializer(allow_null=True)
    text = serializers.SerializerMethodField()
    payload = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "id",
            "gathering",
            "kind",
            "system_event",
            "author",
            "text",
            "payload",
            "is_hidden",
            "created_at",
        ]

    def get_text(self, obj) -> str:
        return HIDDEN_TEXT if obj.is_hidden else obj.text

    def get_payload(self, obj) -> dict:
        return {} if obj.is_hidden else obj.payload


class MessageCreateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=MESSAGE_MAX_LENGTH, trim_whitespace=True)
