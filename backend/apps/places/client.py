"""Клиент API 2ГИС (httpx). Ключ не уходит на клиент. Условия и лимиты — открытый вопрос."""


def search(query: str, *, lat: float | None = None, lng: float | None = None) -> list[dict]:
    """Вернуть [{external_id, name, address, district, lat, lng}]. Кэш в Redis."""
    raise NotImplementedError
