from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from .models import Category, Item


class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title/date", {"fields": ["item_name", "date_published"]}),
        ("URL", {"fields": ["item_slug"]}),
        ("Parent Element", {"fields": ["category_name"]}),
        ("Content (Width ~600px)", {"fields": ["summary", "content"]}),
    ]
    # Overwrite properties for TextFields only
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Category details",
            {"fields": ["category_name", "summary", "image", "category_slug"]},
        )
    ]


# Register your models here.
admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
