from rest_framework.views import APIView


class ReportCreateView(APIView):
    """POST /reports"""

    def post(self, request):
        raise NotImplementedError


class BlockCreateView(APIView):
    """POST /blocks"""

    def post(self, request):
        raise NotImplementedError


class BlockDeleteView(APIView):
    """DELETE /blocks/{userId}"""

    def delete(self, request, user_id):
        raise NotImplementedError
