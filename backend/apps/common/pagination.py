from rest_framework.pagination import CursorPagination


class DefaultCursorPagination(CursorPagination):
    page_size = 20
    ordering = "-created_at"


class StartsAtCursorPagination(CursorPagination):
    """Лента сборов: по времени начала."""

    page_size = 20
    ordering = "starts_at"
