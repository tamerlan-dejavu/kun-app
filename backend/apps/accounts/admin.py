from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import AuthCode, User, UserSession


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # TODO: карточка пользователя с историей сборов и жалоб, inline санкций (раздел 3.7)
    ordering = ["-date_joined"]
    list_display = [
        "phone",
        "name",
        "university",
        "role",
        "reliability",
        "date_joined",
        "is_active",
    ]
    list_filter = ["role", "is_active", "is_staff", "university"]
    search_fields = ["phone", "name"]
    filter_horizontal = ["interests", "groups", "user_permissions"]
    readonly_fields = ["date_joined", "last_login"]
    fieldsets = [
        (None, {"fields": ["phone", "password"]}),
        ("Профиль", {"fields": ["name", "photo", "university", "interests"]}),
        (
            "Онбординг",
            {"fields": ["adult_confirmed_at", "terms_accepted_at", "onboarding_completed_at"]},
        ),
        ("Надёжность", {"fields": ["reliability", "happened_gatherings_count"]}),
        (
            "Доступ",
            {
                "fields": [
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ]
            },
        ),
        ("Даты", {"fields": ["date_joined", "last_login", "deleted_at"]}),
    ]
    add_fieldsets = [(None, {"classes": ["wide"], "fields": ["phone", "password1", "password2"]})]


@admin.register(AuthCode)
class AuthCodeAdmin(admin.ModelAdmin):
    list_display = ["phone", "created_at", "expires_at", "attempts", "locked_until", "used_at"]
    search_fields = ["phone"]
    readonly_fields = [f.name for f in AuthCode._meta.fields]


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ["user", "user_agent", "ip", "created_at", "last_seen_at"]
    raw_id_fields = ["user"]
