from rest_framework.views import APIView


class MessageListCreateView(APIView):
    """GET /gatherings/{id}/messages — история (курсор); POST — отправка. Только участник."""

    def get(self, request, pk):
        raise NotImplementedError

    def post(self, request, pk):
        raise NotImplementedError
