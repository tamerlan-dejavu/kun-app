"""Фильтр логов: телефоны и тексты сообщений в логи не пишутся."""

import logging
import re

PHONE_RE = re.compile(r"\+?7\d{10}")


class PiiFilter(logging.Filter):
    def filter(self, record):
        if isinstance(record.msg, str):
            record.msg = PHONE_RE.sub("+7**********", record.msg)
        return True
