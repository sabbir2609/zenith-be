from django.contrib import admin
from .models import Category, Post
from ckeditor.widgets import CKEditorWidget
from django.db import models


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "created_at",
    )
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "author",
        "category",
        "created_at",
    )
    prepopulated_fields = {"slug": ("title",)}
    formfield_overrides = {
        models.TextField: {"widget": CKEditorWidget()},
    }
