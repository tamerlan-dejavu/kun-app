from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

api_v1 = [
    path("", include("apps.common.urls")),
    path("", include("apps.accounts.urls")),
    path("", include("apps.gatherings.urls")),
    path("", include("apps.chat.urls")),
    path("", include("apps.notifications.urls")),
    path("", include("apps.moderation.urls")),
    path("", include("apps.places.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(api_v1)),
]
