from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class GatheringListCreateView(APIView):
    """GET /gatherings — лента; POST /gatherings — создать сбор."""

    def get(self, request):
        raise NotImplementedError

    def post(self, request):
        raise NotImplementedError


class GatheringDetailView(APIView):
    """GET /gatherings/{id}; PATCH — только создатель."""

    def get(self, request, pk):
        raise NotImplementedError

    def patch(self, request, pk):
        raise NotImplementedError


class GatheringCancelView(APIView):
    """POST /gatherings/{id}/cancel — создатель, с причиной."""

    def post(self, request, pk):
        raise NotImplementedError


class GatheringJoinView(APIView):
    """POST /gatherings/{id}/join"""

    def post(self, request, pk):
        raise NotImplementedError


class GatheringLeaveView(APIView):
    """POST /gatherings/{id}/leave"""

    def post(self, request, pk):
        raise NotImplementedError


class AttendanceView(APIView):
    """POST /gatherings/{id}/attendance — «Я пришёл», участник."""

    def post(self, request, pk):
        raise NotImplementedError


class RatingsView(APIView):
    """POST /gatherings/{id}/ratings — участник."""

    def post(self, request, pk):
        raise NotImplementedError


class MyGatheringsView(APIView):
    """GET /me/gatherings — будущие и прошедшие."""

    def get(self, request):
        raise NotImplementedError


class PublicGatheringView(APIView):
    """GET /public/gatherings/{slug} — без личных данных, для SSR и Open Graph."""

    permission_classes = [AllowAny]

    def get(self, request, slug):
        raise NotImplementedError
