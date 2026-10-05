from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class NotificationSettingsView(APIView):
    """GET/PATCH /me/notifications/settings"""

    def get(self, request):
        raise NotImplementedError

    def patch(self, request):
        raise NotImplementedError


class PushSubscriptionView(APIView):
    """POST /me/push-subscriptions"""

    def post(self, request):
        raise NotImplementedError


class TelegramLinkView(APIView):
    """POST /telegram/link — вернуть ссылку t.me/<bot>?start=<token>."""

    def post(self, request):
        raise NotImplementedError


class TelegramWebhookView(APIView):
    """POST /telegram/webhook — проверка X-Telegram-Bot-Api-Secret-Token."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        raise NotImplementedError
