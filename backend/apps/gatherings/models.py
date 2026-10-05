from django.contrib.gis.db import models


class Gathering(models.Model):
    """Сбор: что, где, когда, сколько мест.

    Поля (разделы 3.3 и 6 ТЗ):
        slug                 — для /g/<slug>
        creator              — FK User (роль может передаваться)
        category             — FK catalog.Category
        title                — до 60 символов
        comment              — до 300 символов
        place_name, address, district
        place_external_id    — id места в 2ГИС
        location             — PointField (PostGIS), сортировка по расстоянию
        starts_at            — UTC, от +1 часа до +14 дней
        seats                — 3–6
        students_only        — bool
        university           — FK, только для students_only
        status               — open | full | cancelled | finished
        moderation_status    — published | pending | hidden
        cancel_reason, cancelled_at
    """

    # TODO


class Participation(models.Model):
    """Участие: user, gathering, joined_at, left_at, is_creator, late_cancel."""

    # TODO: unique (gathering, user) среди активных


class Attendance(models.Model):
    """Отметка «Я пришёл» — от начала до +12 часов. Событие attendance_marked в аналитику."""

    # TODO: gathering, user, marked_at


class Rating(models.Model):
    """Оценка участника: «Пришёл, всё хорошо» / «Не пришёл». Оцениваемый не видит автора."""

    # TODO: gathering, rater, ratee, value (ok | no_show), unique (gathering, rater, ratee)
