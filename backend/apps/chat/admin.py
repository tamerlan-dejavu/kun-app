from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    # TODO: действие «скрыть сообщение» с обязательной причиной и записью в журнал
    list_display = [
        "gathering",
        "author",
        "kind",
        "system_event",
        "short_text",
        "is_hidden",
        "created_at",
    ]
    list_filter = ["kind", "is_hidden"]
    raw_id_fields = ["gathering", "author"]

    @admin.display(description="текст")
    def short_text(self, obj):
        return obj.text[:60]
