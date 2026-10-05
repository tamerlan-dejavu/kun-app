"""Два одновременных «Иду» на последнее место (раздел 9 ТЗ).

Настоящие параллельные транзакции в PostgreSQL: select_for_update должен пропустить
только одного, второй получает «мест нет».
"""

import threading

import pytest
from django.db import connection

from apps.common.exceptions import KunError
from apps.gatherings import services
from apps.gatherings.models import Gathering
from tests.factories import GatheringFactory, ParticipationFactory, UserFactory


@pytest.mark.django_db(transaction=True)
def test_two_concurrent_joins_for_last_seat():
    g = GatheringFactory(seats=3)
    ParticipationFactory(gathering=g, user=g.creator, is_creator=True)
    ParticipationFactory(gathering=g)  # осталось одно место
    racers = [UserFactory(), UserFactory()]

    barrier = threading.Barrier(len(racers))
    results = []

    def join(user):
        try:
            barrier.wait()
            services.join_gathering(Gathering.objects.get(pk=g.pk), user)
            results.append("ok")
        except KunError as e:
            results.append(e.code)
        finally:
            connection.close()

    threads = [threading.Thread(target=join, args=(u,)) for u in racers]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert sorted(results) == ["gathering_full", "ok"]
    g.refresh_from_db()
    assert g.status == "full"
    assert g.participations.filter(left_at__isnull=True).count() == 3
