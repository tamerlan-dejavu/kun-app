class BlockedUserMiddleware:
    """Разлогинивает заблокированных и удалённых пользователей."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # TODO: проверить moderation.UserSanction и deleted_at
        return self.get_response(request)
