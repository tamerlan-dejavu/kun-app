from django.contrib import admin

from .models import BannedWord, Block, ModerationLog, Report, UserSanction

# TODO (раздел 3.7 ТЗ): действия «скрыть», «предупредить», «пауза 7 дней», «заблокировать»
#   с обязательной причиной (admin_forms.ActionReasonForm) и записью в ModerationLog;
#   доступ по роли moderator / admin.


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "target_type",
        "reason",
        "priority",
        "status",
        "created_at",
        "assigned_to",
    ]
    list_filter = ["status", "priority", "target_type", "reason"]
    ordering = ["status", "priority", "created_at"]
    raw_id_fields = ["reporter", "target_user", "target_gathering", "target_message", "assigned_to"]


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ["blocker", "blocked", "created_at"]
    raw_id_fields = ["blocker", "blocked"]


@admin.register(UserSanction)
class UserSanctionAdmin(admin.ModelAdmin):
    list_display = ["user", "kind", "ends_at", "revoked_at", "created_by", "created_at"]
    list_filter = ["kind"]
    raw_id_fields = ["user", "created_by"]


@admin.register(BannedWord)
class BannedWordAdmin(admin.ModelAdmin):
    list_display = ["word", "is_active", "created_at"]
    list_editable = ["is_active"]
    search_fields = ["word"]


@admin.register(ModerationLog)
class ModerationLogAdmin(admin.ModelAdmin):
    """Только чтение: журнал неизменяем (ещё и триггером в БД)."""

    list_display = ["created_at", "actor", "action", "target_type", "target_id", "reason"]
    list_filter = ["action", "target_type"]
    search_fields = ["reason"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
