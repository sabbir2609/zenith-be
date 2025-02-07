from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import Inventory, Role, Staff, Task, TaskCheckList


@admin.register(Role)
class RoleAdmin(ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "stuff_count")

    def stuff_count(self, obj):
        return obj.staff_set.count()


@admin.register(Staff)
class StuffAdmin(ModelAdmin):
    list_display = ("user", "staff_id", "role", "staff_status")
    autocomplete_fields = ("user", "role")
    list_filter = ("staff_status",)
    search_fields = ("user__first_name", "staff_id")
    readonly_fields = ("staff_id",)


class InlineTaskCheckList(TabularInline):
    model = TaskCheckList
    extra = 1


@admin.register(Task)
class TaskAdmin(ModelAdmin):
    list_display = (
        "task_id",
        "staff",
        "assigned_room",
        "task_status",
    )
    autocomplete_fields = ("staff",)
    list_filter = ("task_status",)
    inlines = [InlineTaskCheckList]
    list_per_page = 10


@admin.register(Inventory)
class InventoryAdmin(ModelAdmin):
    list_display = (
        "item_name",
        "item_quantity",
        "created_at",
    )
    search_fields = ("item_name",)
    list_per_page = 10
