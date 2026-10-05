from rest_framework.views import APIView


class PlaceSearchView(APIView):
    """GET /places/search?q= — прокси к 2ГИС."""

    def get(self, request):
        raise NotImplementedError
