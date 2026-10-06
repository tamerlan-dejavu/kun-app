from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView

from .models import Category, Interest
from .serializers import CategorySerializer, InterestSerializer

TAGS = ["catalog"]


class CategoryListView(ListAPIView):
    """GET /catalog/categories — активные категории сборов (фильтр ленты, создание сбора)."""

    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_active=True)
    pagination_class = None

    @extend_schema(tags=TAGS, summary="Категории сборов")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class InterestListView(ListAPIView):
    """GET /catalog/interests — интересы для профиля (онбординг)."""

    serializer_class = InterestSerializer
    queryset = Interest.objects.filter(is_active=True)
    pagination_class = None

    @extend_schema(tags=TAGS, summary="Интересы")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
