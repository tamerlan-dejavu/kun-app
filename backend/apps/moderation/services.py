"""Жалобы и блокировки (раздел 3.7 ТЗ). Действия модератора — с причиной и записью в журнал."""

from django.db import transaction

from apps.common.exceptions import KunError

from .models import Block, Report

# Причина -> приоритет в очереди модератора
PRIORITY_BY_REASON = {
    Report.Reason.DANGER: Report.Priority.CRITICAL,
    Report.Reason.UNDERAGE: Report.Priority.CRITICAL,
    Report.Reason.HARASSMENT: Report.Priority.HIGH,
}


def hide_message(message, actor, reason: str):
    raise NotImplementedError


def hide_gathering(gathering, actor, reason: str):
    raise NotImplementedError


def warn(user, actor, reason: str):
    raise NotImplementedError


def pause(user, actor, reason: str, days: int = 7):
    raise NotImplementedError


def ban(user, actor, reason: str):
    raise NotImplementedError


def _resolve_target(reporter, target_type: str, target_id: int) -> dict:
    """Цель жалобы должна существовать и быть видна автору."""
    from apps.accounts.models import User
    from apps.chat.models import Message
    from apps.gatherings.models import Participation
    from apps.gatherings.selectors import visible_gatherings

    not_found = KunError("target_not_found", "Не нашли, на что жалоба", 404)
    if target_type == Report.TargetType.USER:
        if target_id == reporter.pk:
            raise KunError("report_self", "На себя пожаловаться нельзя")
        user = User.objects.filter(pk=target_id, deleted_at__isnull=True).first()
        if not user:
            raise not_found
        return {"target_user": user}
    if target_type == Report.TargetType.GATHERING:
        gathering = visible_gatherings(reporter).filter(pk=target_id).first()
        if not gathering:
            raise not_found
        return {"target_gathering": gathering}
    # Сообщение — только из чата, где автор жалобы участник
    message = Message.objects.filter(pk=target_id, kind=Message.Kind.USER).first()
    if (
        not message
        or not Participation.objects.filter(
            gathering_id=message.gathering_id, user=reporter
        ).exists()
    ):
        raise not_found
    if message.author_id == reporter.pk:
        raise KunError("report_self", "На своё сообщение пожаловаться нельзя")
    return {"target_message": message}


@transaction.atomic
def create_report(reporter, target_type, target_id, reason, text="") -> Report:
    """Повторная открытая жалоба на ту же цель не дублируется.
    Критичные (угроза, младше 18) сразу уходят в Telegram-чат модераторов."""
    target = _resolve_target(reporter, target_type, target_id)
    existing = Report.objects.filter(
        reporter=reporter, target_type=target_type, status__in=["new", "in_review"], **target
    ).first()
    if existing:
        return existing

    report = Report.objects.create(
        reporter=reporter,
        target_type=target_type,
        reason=reason,
        text=text,
        priority=PRIORITY_BY_REASON.get(reason, Report.Priority.NORMAL),
        **target,
    )
    if report.priority == Report.Priority.CRITICAL:
        from .tasks import alert_moderators

        transaction.on_commit(lambda: alert_moderators.delay(report.pk))
    return report


def block_user(blocker, blocked_id: int) -> Block:
    """Блокировка в обе стороны: не видят сборы друг друга, не попадают в один сбор."""
    from apps.accounts.models import User

    if blocked_id == blocker.pk:
        raise KunError("block_self", "Себя заблокировать нельзя")
    if not User.objects.filter(pk=blocked_id, deleted_at__isnull=True).exists():
        raise KunError("user_not_found", "Не нашли такого пользователя", 404)
    block, _ = Block.objects.get_or_create(blocker=blocker, blocked_id=blocked_id)
    return block


def unblock_user(blocker, blocked_id: int) -> None:
    Block.objects.filter(blocker=blocker, blocked_id=blocked_id).delete()
