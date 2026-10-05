from django.contrib import admin

from .models import University


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ["short_name", "name", "city", "sort_order", "is_active"]
    list_editable = ["sort_order", "is_active"]
    list_filter = ["city", "is_active"]
    search_fields = ["name", "short_name"]
