"""Правила сборов (раздел 3.3 и 3.6 ТЗ).

Всё, что меняет состав участников, — в transaction.atomic с select_for_update на строке сбора:
два одновременных «Иду» на последнее место выстраиваются в очередь, второй получает «мест нет».

Уведомления ставятся в очередь после коммита (notifications.dispatcher).
TODO: события аналитики (analytics.events) — вместе с этим модулем.
"""

from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from apps.chat.models import Message
from apps.chat.services import post_system_message
from apps.common.exceptions import KunError
from apps.common.permissions import ensure_can_act
from apps.moderation.text_check import contains_banned_words
from apps.notifications.dispatcher import gathering_context, notify
from apps.notifications.types import NotificationType

from .models import Attendance, Gathering, Participation, Rating
from .selectors import blocked_user_ids

RULES = settings.KUN
ACTIVE_STATUSES = (Gathering.Status.OPEN, Gathering.Status.FULL)
EDITABLE_FIELDS = {
    "starts_at",
    "comment",
    "place_name",
    "address",
    "district",
    "place_external_id",
    "location",
}


# --- проверки -----------------------------------------------------------------------------


def _check_starts_at(starts_at):
    now = timezone.now()
    if starts_at < now + timedelta(hours=RULES["GATHERING_MIN_LEAD_HOURS"]):
        raise KunError("starts_too_soon", "Сбор можно создать минимум за час до начала")
    if starts_at > now + timedelta(days=RULES["GATHERING_MAX_LEAD_DAYS"]):
        raise KunError("starts_too_late", "Сбор можно создать не дальше чем на 14 дней вперёд")


def _active_participation(gathering, user):
    return Participation.objects.filter(
        gathering=gathering, user=user, left_at__isnull=True
    ).first()


def _require_participant(gathering, user):
    participation = _active_participation(gathering, user)
    if participation is None:
        raise KunError("not_participant", "Это доступно только участникам сбора", 403)
    return participation


def _require_creator(gathering, user):
    if gathering.creator_id != user.pk:
        raise KunError("not_creator", "Это может только создатель сбора", 403)


def _active_count(gathering) -> int:
    return gathering.participations.filter(left_at__isnull=True).count()


def _member_ids(gathering, exclude=None) -> list[int]:
    ids = gathering.participations.filter(left_at__isnull=True).values_list("user_id", flat=True)
    return [uid for uid in ids if uid != getattr(exclude, "pk", None)]


def _lock(gathering) -> Gathering:
    """Перечитать сбор с блокировкой строки до конца транзакции."""
    return Gathering.objects.select_for_update().get(pk=gathering.pk)


# --- создание и изменение -------------------------------------------------------------------


@transaction.atomic
def create_gathering(user, data: dict) -> Gathering:
    """Лимит 3 активных на создателя, окно времени +1 ч…+14 дней, место только из поиска.
    Запрещённые слова в названии или комментарии — сбор уходит на проверку (pending)."""
    ensure_can_act(user)
    _check_starts_at(data["starts_at"])

    active = Gathering.objects.filter(
        creator=user, status__in=ACTIVE_STATUSES, starts_at__gt=timezone.now()
    ).count()
    if active >= RULES["GATHERING_ACTIVE_PER_CREATOR"]:
        raise KunError("too_many_active", "У тебя уже 3 активных сбора — дождись, пока они пройдут")

    pending = contains_banned_words(data.get("title", ""), data.get("comment", ""))
    gathering = Gathering.objects.create(
        creator=user,
        moderation_status=(
            Gathering.ModerationStatus.PENDING if pending else Gathering.ModerationStatus.PUBLISHED
        ),
        **data,
    )
    Participation.objects.create(gathering=gathering, user=user, is_creator=True)
    return gathering


@transaction.atomic
def update_gathering(gathering, user, data: dict) -> Gathering:
    """Создатель меняет время, место, комментарий.
    В чат — системное сообщение со списком изменений."""
    gathering = _lock(gathering)
    _require_creator(gathering, user)
    if gathering.status not in ACTIVE_STATUSES or gathering.starts_at <= timezone.now():
        raise KunError("not_editable", "Этот сбор уже нельзя изменить")

    changes = {k: v for k, v in data.items() if k in EDITABLE_FIELDS}
    if "starts_at" in changes:
        _check_starts_at(changes["starts_at"])
    changed = [k for k, v in changes.items() if getattr(gathering, k) != v]
    if not changed:
        return gathering

    for key in changed:
        setattr(gathering, key, changes[key])
    if "comment" in changed and contains_banned_words(gathering.title, gathering.comment):
        gathering.moderation_status = Gathering.ModerationStatus.PENDING
        changed.append("moderation_status")
    gathering.save(update_fields=[*changed, "updated_at"])

    visible = [
        f for f in changed if f not in ("location", "place_external_id", "moderation_status")
    ]
    post_system_message(gathering, Message.SystemEvent.UPDATED, {"fields": visible})
    notify(
        _member_ids(gathering, exclude=user), NotificationType.UPDATED, gathering_context(gathering)
    )
    return gathering


@transaction.atomic
def cancel_gathering(gathering, user, reason: str) -> Gathering:
    """Отмена создателем с причиной. Участникам — уведомление (выключить нельзя),
    а если до начала меньше 3 часов — ещё и SMS."""
    gathering = _lock(gathering)
    _require_creator(gathering, user)
    if gathering.status not in ACTIVE_STATUSES:
        raise KunError("not_cancellable", "Этот сбор уже не отменить")

    now = timezone.now()
    gathering.status = Gathering.Status.CANCELLED
    gathering.cancel_reason = reason
    gathering.cancelled_at = now
    gathering.save(update_fields=["status", "cancel_reason", "cancelled_at", "updated_at"])
    post_system_message(gathering, Message.SystemEvent.CANCELLED, {"reason": reason})
    urgent = gathering.starts_at - now < timedelta(hours=RULES["SMS_CANCEL_THRESHOLD_HOURS"])
    notify(
        _member_ids(gathering, exclude=user),
        NotificationType.CANCELLED,
        gathering_context(gathering, reason=reason),
        sms=urgent,
    )
    return gathering


# --- участие ---------------------------------------------------------------------------------


@transaction.atomic
def join_gathering(gathering, user) -> Participation:
    """Одна транзакция: статус и время, свободные места, блокировки с участниками."""
    ensure_can_act(user)
    gathering = _lock(gathering)

    if gathering.moderation_status != Gathering.ModerationStatus.PUBLISHED:
        raise KunError("not_published", "Сбор ещё на проверке")
    if gathering.status == Gathering.Status.FULL:
        raise KunError("gathering_full", "Мест больше нет")
    if gathering.status != Gathering.Status.OPEN or gathering.starts_at <= timezone.now():
        raise KunError("gathering_closed", "К этому сбору уже не присоединиться")
    if _active_participation(gathering, user):
        raise KunError("already_joined", "Ты уже в этом сборе")

    member_ids = set(
        gathering.participations.filter(left_at__isnull=True).values_list("user_id", flat=True)
    )
    if member_ids & blocked_user_ids(user):
        # Не раскрываем, кто именно: просто «нельзя»
        raise KunError("blocked", "К этому сбору присоединиться нельзя", 403)

    count = len(member_ids)
    if count >= gathering.seats:
        raise KunError("gathering_full", "Мест больше нет")

    participation = Participation.objects.create(gathering=gathering, user=user)
    if count + 1 >= gathering.seats:
        gathering.status = Gathering.Status.FULL
        gathering.save(update_fields=["status", "updated_at"])
    post_system_message(
        gathering, Message.SystemEvent.JOINED, {"user_id": user.pk, "name": user.name}
    )
    notify(
        [gathering.creator_id],
        NotificationType.JOINED_LEFT,
        gathering_context(gathering, joined=True, actor=user.name),
    )
    return participation


@transaction.atomic
def leave_gathering(gathering, user) -> Gathering:
    """Выход до начала. Меньше чем за 2 часа — поздний выход, снижает надёжность.

    Если выходит создатель — роль переходит к тому, кто присоединился раньше всех.
    Если никого не осталось — сбор отменяется.
    TODO: сверить с крайними случаями вкладки «User flows».
    """
    gathering = _lock(gathering)
    participation = _require_participant(gathering, user)
    now = timezone.now()
    if gathering.status not in ACTIVE_STATUSES or gathering.starts_at <= now:
        raise KunError("not_leavable", "Из этого сбора уже не выйти")

    participation.left_at = now
    participation.late_leave = gathering.starts_at - now < timedelta(
        hours=RULES["LATE_CANCEL_HOURS"]
    )
    was_creator = participation.is_creator
    participation.is_creator = False
    participation.save(update_fields=["left_at", "late_leave", "is_creator"])
    post_system_message(
        gathering, Message.SystemEvent.LEFT, {"user_id": user.pk, "name": user.name}
    )

    remaining = gathering.participations.filter(left_at__isnull=True).order_by("joined_at", "pk")
    if not remaining.exists():
        gathering.status = Gathering.Status.CANCELLED
        gathering.cancel_reason = "Все участники вышли"
        gathering.cancelled_at = now
        gathering.save(update_fields=["status", "cancel_reason", "cancelled_at", "updated_at"])
        post_system_message(
            gathering, Message.SystemEvent.CANCELLED, {"reason": gathering.cancel_reason}
        )
        return gathering

    update_fields = ["updated_at"]
    if gathering.status == Gathering.Status.FULL:
        gathering.status = Gathering.Status.OPEN
        update_fields.append("status")
    if not was_creator:
        notify(
            [gathering.creator_id],
            NotificationType.JOINED_LEFT,
            gathering_context(gathering, joined=False, actor=user.name),
        )
    else:
        heir = remaining.select_related("user").first()
        heir.is_creator = True
        heir.save(update_fields=["is_creator"])
        gathering.creator = heir.user
        update_fields.append("creator")
        post_system_message(
            gathering,
            Message.SystemEvent.CREATOR_CHANGED,
            {"user_id": heir.user_id, "name": heir.user.name},
        )
    gathering.save(update_fields=update_fields)
    return gathering


# --- после встречи ---------------------------------------------------------------------------


def _check_after_window(gathering, hours: int, what: str):
    now = timezone.now()
    if gathering.status == Gathering.Status.CANCELLED:
        raise KunError("gathering_cancelled", "Сбор отменён")
    if now < gathering.starts_at:
        raise KunError("too_early", f"{what} — после начала сбора")
    if now > gathering.starts_at + timedelta(hours=hours):
        raise KunError("too_late", f"{what} — в течение {hours} часов после начала")


def mark_attendance(gathering, user) -> Attendance:
    """«Я пришёл» — от начала до +12 часов. Повторная отметка ничего не меняет."""
    _require_participant(gathering, user)
    _check_after_window(gathering, RULES["ATTENDANCE_WINDOW_HOURS"], "Отметиться можно")
    attendance, _ = Attendance.objects.get_or_create(gathering=gathering, user=user)
    return attendance


@transaction.atomic
def submit_ratings(gathering, user, ratings: list[dict]) -> list[Rating]:
    """Оценки участникам: ok / no_show. Повторная оценка того же человека её заменяет.
    TODO: пересчёт надёжности (reliability.recalculate), когда команда утвердит формулу."""
    _require_participant(gathering, user)
    _check_after_window(gathering, RULES["RATING_WINDOW_HOURS"], "Оценить можно")

    member_ids = set(
        gathering.participations.filter(left_at__isnull=True).values_list("user_id", flat=True)
    )
    result = []
    for item in ratings:
        ratee_id = item["user_id"]
        if ratee_id == user.pk:
            raise KunError("rate_self", "Себя оценивать не нужно")
        if ratee_id not in member_ids:
            raise KunError("not_participant", "Можно оценить только участников этого сбора")
        rating, _ = Rating.objects.update_or_create(
            gathering=gathering, rater=user, ratee_id=ratee_id, defaults={"value": item["value"]}
        )
        result.append(rating)
    return result
