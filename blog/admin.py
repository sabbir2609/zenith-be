from django.contrib import admin
from django.db import models
from django.contrib.postgres.fields import ArrayField
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget
from unfold.contrib.filters.admin import (
    RangeDateFilter,
    RangeDateTimeFilter,  # noqa
)
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = (
        "name",
        "slug",
        "created_at",
    )
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "created_at",
    )
    prepopulated_fields = {"slug": ("title",)}
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
        ArrayField: {"widget": ArrayWidget},
    }
    list_filter = (
        ("created_at", RangeDateFilter),
        ("updated_at", RangeDateFilter),
        "category",
    )
    list_editable = ("category",)

    list_filter_submit = True
    search_fields = ("title", "content")

    export_form = ExportForm
    import_form = ImportForm
