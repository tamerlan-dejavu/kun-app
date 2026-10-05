from django.contrib import admin

from .models import Category, Interest


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "emoji", "slug", "sort_order", "is_active"]
    list_editable = ["sort_order", "is_active"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "sort_order", "is_active"]
    list_editable = ["sort_order", "is_active"]
    prepopulated_fields = {"slug": ["name"]}
