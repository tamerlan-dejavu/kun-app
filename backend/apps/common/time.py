"""Хранение в UTC, показ в Asia/Almaty."""

from zoneinfo import ZoneInfo

ALMATY = ZoneInfo("Asia/Almaty")


def to_almaty(dt):
    return dt.astimezone(ALMATY)
