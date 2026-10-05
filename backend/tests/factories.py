"""factory_boy-фабрики для тестов."""

from datetime import timedelta

import factory
from django.contrib.gis.geos import Point
from django.utils import timezone

from apps.accounts.models import User
from apps.catalog.models import Category
from apps.chat.models import Message
from apps.gatherings.models import Gathering, Participation


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    phone = factory.Sequence(lambda n: f"+7701{n:07d}")
    name = factory.Faker("first_name", locale="ru_RU")


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ["slug"]

    slug = "test-category"
    name = "Тестовая категория"


class GatheringFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Gathering

    creator = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    title = "Тестовый сбор"
    place_name = "Нархоз"
    address = "ул. Жандосова, 55"
    district = "Ауэзовский"
    place_external_id = factory.Sequence(lambda n: f"test-{n}")
    location = Point(76.874, 43.2215, srid=4326)
    starts_at = factory.LazyFunction(lambda: timezone.now() + timedelta(days=1))
    seats = 4


class ParticipationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Participation

    gathering = factory.SubFactory(GatheringFactory)
    user = factory.SubFactory(UserFactory)


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    gathering = factory.SubFactory(GatheringFactory)
    author = factory.SubFactory(UserFactory)
    text = "Привет"
