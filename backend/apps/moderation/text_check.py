"""Автопроверка текста сбора по списку запрещённых слов (раздел 3.3 ТЗ)."""

import re

# Латиница, похожая на кириллицу: «кaзино» с латинской «a» тоже ловим
LOOKALIKES = str.maketrans("aeopcyxkmtbh", "аеорсухкмтвн")
WORD_RE = re.compile(r"[^\wё]+", re.UNICODE)


def normalize(text: str) -> str:
    text = text.lower().replace("ё", "е").translate(LOOKALIKES)
    return " " + WORD_RE.sub(" ", text).strip() + " "


def contains_banned_words(*texts: str) -> bool:
    """Ищет запрещённые слова и фразы с начала слова: «казино» ловит и «казиношка»."""
    from apps.moderation.models import BannedWord

    haystack = normalize(" ".join(t for t in texts if t))
    for word in BannedWord.objects.filter(is_active=True).values_list("word", flat=True):
        needle = normalize(word).strip()
        if needle and f" {needle}" in haystack:
            return True
    return False
