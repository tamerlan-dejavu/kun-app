"""Фото профиля (раздел 3.2 и 4 ТЗ): до 5 МБ, JPG/PNG/WebP, обрезка до квадрата,
пересохранение сервером без EXIF (в том числе геометок)."""

from io import BytesIO

from django.conf import settings
from django.core.files.base import ContentFile
from PIL import Image, ImageOps, UnidentifiedImageError

from apps.common.exceptions import KunError

ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP"}
AVATAR_SIZE = 512
# Защита от «бомб»: картинка в несколько КБ, которая разворачивается в гигапиксели
Image.MAX_IMAGE_PIXELS = 40_000_000


def process_avatar(uploaded_file) -> ContentFile:
    """Проверить и пересохранить фото. Возвращает квадрат 512x512 в WebP без метаданных."""
    if uploaded_file.size > settings.KUN["PHOTO_MAX_BYTES"]:
        raise KunError("photo_too_large", "Фото больше 5 МБ — выбери поменьше")

    try:
        probe = Image.open(uploaded_file)
        fmt = probe.format
        probe.verify()  # битый файл падает здесь
        uploaded_file.seek(0)
        image = Image.open(uploaded_file)
        image.load()
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError):
        raise KunError("photo_invalid", "Не получилось открыть фото") from None
    if fmt not in ALLOWED_FORMATS:
        raise KunError("photo_format", "Подойдут JPG, PNG или WebP")

    image = ImageOps.exif_transpose(image)  # фото с телефона — с правильным поворотом
    image = image.convert("RGB")
    image = ImageOps.fit(image, (AVATAR_SIZE, AVATAR_SIZE), Image.Resampling.LANCZOS)

    out = BytesIO()
    # Новое изображение: EXIF и прочие метаданные исходника в него не переносятся
    image.save(out, "WEBP", quality=85, method=6)
    return ContentFile(out.getvalue(), name="avatar.webp")
