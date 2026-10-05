from django.contrib import admin

from .models import NotificationSettings, PushSubscription, TelegramLink


@admin.register(NotificationSettings)
class NotificationSettingsAdmin(admin.ModelAdmin):
    list_display = ["user", "joined_left", "chat_message", "reminder", "updated", "after_prompt"]
    raw_id_fields = ["user"]


@admin.register(PushSubscription)
class PushSubscriptionAdmin(admin.ModelAdmin):
    list_display = ["user", "kind", "user_agent", "created_at", "last_used_at"]
    list_filter = ["kind"]
    raw_id_fields = ["user"]


@admin.register(TelegramLink)
class TelegramLinkAdmin(admin.ModelAdmin):
    list_display = ["user", "chat_id", "linked_at"]
    raw_id_fields = ["user"]
