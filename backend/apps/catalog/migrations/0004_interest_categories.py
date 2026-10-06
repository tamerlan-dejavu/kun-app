"""Стартовая связь «интерес → категории сборов» для подбора «Для тебя».
Дальше её правит администратор в /admin (Интересы -> категории)."""

from django.db import migrations

MAPPING = {
    "movies": ["cinema"],
    "music": ["concert"],
    "board-games": ["board-games"],
    "video-games": ["board-games", "club"],
    "sport": ["sport"],
    "running": ["sport", "walk"],
    "hiking": ["walk", "sport"],
    "books": ["club", "study", "coffee"],
    "art": ["walk", "club"],
    "photo": ["walk"],
    "food": ["food", "coffee"],
    "coffee": ["coffee"],
    "languages": ["study", "club", "coffee"],
    "tech": ["study", "club"],
    "startups": ["club", "coffee"],
    "dance": ["concert", "club"],
    "standup": ["concert"],
    "volunteering": ["club"],
}


def forward(apps, schema_editor):
    Interest = apps.get_model("catalog", "Interest")
    Category = apps.get_model("catalog", "Category")
    categories = {c.slug: c for c in Category.objects.all()}
    for slug, cats in MAPPING.items():
        interest = Interest.objects.filter(slug=slug).first()
        if interest:
            interest.categories.add(*[categories[c] for c in cats if c in categories])


def backward(apps, schema_editor):
    for interest in apps.get_model("catalog", "Interest").objects.all():
        interest.categories.clear()


class Migration(migrations.Migration):
    dependencies = [("catalog", "0003_for_you")]

    operations = [migrations.RunPython(forward, backward)]
