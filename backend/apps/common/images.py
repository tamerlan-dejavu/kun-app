"""Обработка фото: проверка формата и размера, обрезка до квадрата, ресайз, удаление EXIF."""

ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP"}
AVATAR_SIZE = 512


def process_avatar(uploaded_file):
    """Пересохранить фото сервером без EXIF (в т. ч. геометок). Возвращает ContentFile в WebP."""
    # TODO: Pillow — open, verify, exif_transpose, crop square, resize, save без metadata
    raise NotImplementedError
