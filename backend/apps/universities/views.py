from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.generics import ListAPIView

from .models import University


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ["id", "name", "short_name", "city"]


class UniversityListView(ListAPIView):
    """GET /catalog/universities — справочник вузов для профиля."""

    serializer_class = UniversitySerializer
    queryset = University.objects.filter(is_active=True)
    pagination_class = None

    @extend_schema(tags=["catalog"], summary="Вузы")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
