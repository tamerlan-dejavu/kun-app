from django.db import models


class Category(models.Model):
    """Категория сбора: кино, прогулка, клуб, настолки... Ведёт администратор."""

    # TODO: slug, name, emoji/icon, order, is_active


class Interest(models.Model):
    """Интерес для профиля (3–5 при онбординге)."""

    # TODO: slug, name, order, is_active
