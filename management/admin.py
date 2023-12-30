from django.contrib import admin
from .models import Task, Stuff, StuffType


@admin.register(StuffType)
class StuffTypeAdmin(admin.ModelAdmin):
    search_fields = ("stuff_type",)


@admin.register(Stuff)
class StuffAdmin(admin.ModelAdmin):
    list_display = ("user", "staff_id", "stuff_type", "status")
    autocomplete_fields = ("user", "stuff_type")
    list_filter = ("status",)
    search_fields = ("user__first_name", "staff_id")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("task_id", "task_description", "stuff", "task_status")
