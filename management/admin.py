from django.contrib import admin
from .models import Task, Staff, Role, TaskCheckList


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    search_fields = ("role",)


@admin.register(Staff)
class StuffAdmin(admin.ModelAdmin):
    list_display = ("user", "staff_id", "role", "staff_status")
    autocomplete_fields = ("user", "role")
    list_filter = ("staff_status",)
    search_fields = ("user__first_name", "staff_id")


class InlineTaskCheckList(admin.TabularInline):
    model = TaskCheckList
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "task_id",
        "staff",
        "task_description",
        "assigned_room",
        "task_status",
    )
    autocomplete_fields = ("staff",)
    list_filter = ("task_status",)
    inlines = [InlineTaskCheckList]
    paginated_by = 10
