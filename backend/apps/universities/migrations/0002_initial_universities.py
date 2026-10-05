"""Стартовый справочник вузов. Остальные добавляет администратор в /admin."""

from django.db import migrations

# (полное название, короткое, город)
UNIVERSITIES = [
    ("Университет Нархоз", "Narxoz", "Алматы"),
    ("Казахский национальный университет имени аль-Фараби", "КазНУ", "Алматы"),
    ("Казахстанско-Британский технический университет", "КБТУ", "Алматы"),
    ("Университет КИМЭП", "KIMEP", "Алматы"),
    ("Satbayev University", "Satbayev", "Алматы"),
    ("Международный университет информационных технологий", "МУИТ", "Алматы"),
    ("Университет имени Сулеймана Демиреля", "SDU", "Алматы"),
    ("Almaty Management University", "AlmaU", "Алматы"),
    ("Казахский национальный медицинский университет имени С. Д. Асфендиярова", "КазНМУ", "Алматы"),
    ("Казахский национальный педагогический университет имени Абая", "КазНПУ", "Алматы"),
    (
        "Казахский университет международных отношений и мировых языков имени Абылай хана",
        "КазУМОиМЯ",
        "Алматы",
    ),
    ("Университет «Туран»", "Туран", "Алматы"),
    ("Алматинский университет энергетики и связи имени Гумарбека Даукеева", "АУЭС", "Алматы"),
    ("Назарбаев Университет", "NU", "Астана"),
    ("Astana IT University", "AITU", "Астана"),
    ("Евразийский национальный университет имени Л. Н. Гумилёва", "ЕНУ", "Астана"),
]


def forward(apps, schema_editor):
    University = apps.get_model("universities", "University")
    for i, (name, short_name, city) in enumerate(UNIVERSITIES):
        University.objects.update_or_create(
            name=name, defaults={"short_name": short_name, "city": city, "sort_order": i * 10}
        )


def backward(apps, schema_editor):
    apps.get_model("universities", "University").objects.filter(
        name__in=[u[0] for u in UNIVERSITIES]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [("universities", "0001_initial")]

    operations = [migrations.RunPython(forward, backward)]
