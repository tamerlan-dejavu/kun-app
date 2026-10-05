from rest_framework.views import APIView


class StudentRequestView(APIView):
    """POST /me/student/request"""

    def post(self, request):
        raise NotImplementedError


class StudentVerifyView(APIView):
    """POST /me/student/verify"""

    def post(self, request):
        raise NotImplementedError
