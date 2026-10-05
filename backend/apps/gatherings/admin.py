from django.contrib import admin

from .models import Attendance, Gathering, Participation, Rating


class ParticipationInline(admin.TabularInline):
    model = Participation
    extra = 0
    raw_id_fields = ["user"]
    readonly_fields = ["joined_at"]


@admin.register(Gathering)
class GatheringAdmin(admin.ModelAdmin):
    # TODO: действие «скрыть сбор» с обязательной причиной и записью в журнал
    list_display = [
        "title",
        "category",
        "starts_at",
        "seats",
        "status",
        "moderation_status",
        "creator",
    ]
    list_filter = ["status", "moderation_status", "category"]
    search_fields = ["title", "slug", "place_name"]
    date_hierarchy = "starts_at"
    raw_id_fields = ["creator"]
    readonly_fields = ["slug", "created_at", "updated_at"]
    inlines = [ParticipationInline]


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ["gathering", "user", "marked_at"]
    raw_id_fields = ["gathering", "user"]


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ["gathering", "ratee", "value", "created_at"]
    list_filter = ["value"]
    raw_id_fields = ["gathering", "rater", "ratee"]
