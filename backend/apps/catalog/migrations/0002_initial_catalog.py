"""Стартовые категории сборов и интересы. Дальше их ведёт администратор в /admin."""

from django.db import migrations

CATEGORIES = [
    ("cinema", "Кино", "🎬"),
    ("walk", "Прогулка", "🚶"),
    ("board-games", "Настолки", "🎲"),
    ("coffee", "Кофе и разговоры", "☕"),
    ("sport", "Спорт", "🏀"),
    ("concert", "Концерт", "🎵"),
    ("club", "Клуб и сообщество", "🤝"),
    ("study", "Учёба вместе", "📚"),
    ("food", "Поесть", "🍜"),
    ("other", "Другое", "✨"),
]

INTERESTS = [
    ("movies", "Кино и сериалы"),
    ("music", "Музыка"),
    ("board-games", "Настольные игры"),
    ("video-games", "Видеоигры"),
    ("sport", "Спорт"),
    ("running", "Бег"),
    ("hiking", "Горы и походы"),
    ("books", "Книги"),
    ("art", "Искусство и выставки"),
    ("photo", "Фото"),
    ("food", "Еда и кафе"),
    ("coffee", "Кофе"),
    ("languages", "Языки"),
    ("tech", "IT и технологии"),
    ("startups", "Стартапы и бизнес"),
    ("dance", "Танцы"),
    ("standup", "Стендап"),
    ("volunteering", "Волонтёрство"),
]


def forward(apps, schema_editor):
    Category = apps.get_model("catalog", "Category")
    Interest = apps.get_model("catalog", "Interest")
    for i, (slug, name, emoji) in enumerate(CATEGORIES):
        Category.objects.update_or_create(
            slug=slug, defaults={"name": name, "emoji": emoji, "sort_order": i * 10}
        )
    for i, (slug, name) in enumerate(INTERESTS):
        Interest.objects.update_or_create(slug=slug, defaults={"name": name, "sort_order": i * 10})


def backward(apps, schema_editor):
    apps.get_model("catalog", "Category").objects.filter(
        slug__in=[c[0] for c in CATEGORIES]
    ).delete()
    apps.get_model("catalog", "Interest").objects.filter(
        slug__in=[i[0] for i in INTERESTS]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [("catalog", "0001_initial")]

    operations = [migrations.RunPython(forward, backward)]
