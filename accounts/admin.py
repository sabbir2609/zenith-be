from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.decorators import display
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .models import User, Permissions, Roles


admin.site.unregister(Group)


# Permissions Model Admin
@admin.register(Permissions)
class PermissionsAdmin(ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name", "description"]
    ordering = ["name"]
    list_filter = ["name"]


# Roles Model Admin
@admin.register(Roles)
class RolesAdmin(ModelAdmin):
    list_display = ["name", "description", "get_permissions"]
    search_fields = ["name", "description"]
    ordering = ["name"]

    # Display permissions associated with each role
    def get_permissions(self, obj):
        return ", ".join([perm.name for perm in obj.permissions.all()])

    get_permissions.short_description = "Permissions"

    filter_horizontal = ("permissions",)


# User Model Admin
@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = [
        "display_header",
        "email",
        "is_active",
        "display_admin",
        "display_superuser",
        "display_created",
    ]
    list_filter = ["is_admin", "is_superuser", "is_active"]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    ("first_name", "last_name"),
                    "email",
                ),
                "classes": ["tab"],
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_admin",
                    "is_superuser",
                    # "groups",
                    # "user_permissions",
                    "role",  # Add the role field here
                ),
                "classes": ["tab"],
            },
        ),
        (
            _("Important dates"),
            {
                "fields": ("last_login",),
                "classes": ["tab"],
            },
        ),
    )
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }
    readonly_fields = ["last_login", "created_at"]

    @display(description=_("User"))
    def display_header(self, instance: User):
        return instance.get_full_name()

    @display(description=_("Admin"), boolean=True)
    def display_admin(self, instance: User):
        return instance.is_admin

    @display(description=_("Superuser"), boolean=True)
    def display_superuser(self, instance: User):
        return instance.is_superuser

    @display(description=_("Created"))
    def display_created(self, instance: User):
        return instance.created_at


# GroupAdmin remains unchanged
@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
