from django.db import models


class University(models.Model):
    """Вуз — справочник для необязательного поля профиля. Ведёт администратор.

    Регистрация открыта всем; вуз ничего не ограничивает и не подтверждается.
    """

    name = models.CharField("название", max_length=200, unique=True)
    short_name = models.CharField(
        "короткое имя", max_length=30, db_comment="для профиля, например Narxoz, КБТУ"
    )
    city = models.CharField("город", max_length=50, default="Алматы")
    sort_order = models.PositiveSmallIntegerField("порядок", default=0)
    is_active = models.BooleanField("активен", default=True)
    created_at = models.DateTimeField("создан", auto_now_add=True)

    class Meta:
        verbose_name = "вуз"
        verbose_name_plural = "вузы"
        ordering = ["sort_order", "short_name"]
        db_table_comment = "Справочник вузов для необязательного поля профиля"

    def __str__(self):
        return self.short_name
