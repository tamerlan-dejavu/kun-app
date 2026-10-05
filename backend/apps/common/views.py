from django.core.cache import cache
from django.db import connection
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def health(request):
    """GET /health — проверка после выкладки и внешний мониторинг.
    503, если БД или Redis недоступны."""
    checks = {}
    try:
        connection.ensure_connection()
        checks["db"] = "ok"
    except Exception:
        checks["db"] = "error"
    try:
        cache.set("health", "ok", 5)
        checks["redis"] = "ok" if cache.get("health") == "ok" else "error"
    except Exception:
        checks["redis"] = "error"

    ok = all(v == "ok" for v in checks.values())
    return Response({"status": "ok" if ok else "error", **checks}, status=200 if ok else 503)
