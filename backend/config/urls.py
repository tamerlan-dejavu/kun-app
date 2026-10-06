from django.conf import settings
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
    path("", include("apps.catalog.urls")),
    path("", include("apps.universities.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(api_v1)),
]

if settings.DEBUG:
    # Только dev: фото из MEDIA_ROOT отдаёт Django (в production — S3)
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Только dev: вход по паролю в браузерный API DRF (/api/v1/auth/dev/login/)
    # под демо-пользователями, пока нет входа по телефону. В production этих URL нет.
    urlpatterns += [path("api/v1/auth/dev/", include("rest_framework.urls"))]
