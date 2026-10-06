from django.db import models


class Category(models.Model):
    """Категория сбора. Ведёт администратор."""

    slug = models.SlugField("код", max_length=50, unique=True)
    name = models.CharField("название", max_length=50)
    emoji = models.CharField("эмодзи", max_length=8, blank=True)
    sort_order = models.PositiveSmallIntegerField("порядок", default=0)
    is_active = models.BooleanField("активна", default=True)

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["sort_order", "name"]
        db_table_comment = "Категории сборов: кино, прогулка, настолки..."

    def __str__(self):
        return self.name


class Interest(models.Model):
    """Интерес для профиля (3–5 при онбординге)."""

    slug = models.SlugField("код", max_length=50, unique=True)
    name = models.CharField("название", max_length=50)
    categories = models.ManyToManyField(
        Category,
        related_name="interests",
        blank=True,
        verbose_name="категории сборов",
        help_text="Какие сборы подходят людям с этим интересом — для подбора «Для тебя»",
    )
    sort_order = models.PositiveSmallIntegerField("порядок", default=0)
    is_active = models.BooleanField("активен", default=True)

    class Meta:
        verbose_name = "интерес"
        verbose_name_plural = "интересы"
        ordering = ["sort_order", "name"]
        db_table_comment = "Интересы для профиля и будущего подбора «Для тебя»"

    def __str__(self):
        return self.name
