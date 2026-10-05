from channels.auth import AuthMiddlewareStack


def SessionAuthMiddlewareStack(inner):  # noqa: N802
    """Сессионная кука Django для WebSocket (этап 3 — добавить JWT из query/header)."""
    return AuthMiddlewareStack(inner)
