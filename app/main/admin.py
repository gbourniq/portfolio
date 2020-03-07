from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from .models import Article, Category, SubCategory


class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title/date", {"fields": ["article_name", "date_published"]}),
        ("URL", {"fields": ["article_slug"]}),
        ("Parent Element", {"fields": ["subcategory_name"]}),
        ("Content", {"fields": ["summary", "content", "image"]}),
    ]
    # Overwrite properties for TextFields only
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }


class SubCategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title", {"fields": ["subcategory_name", "subcategory_slug"]}),
        ("Parent Element", {"fields": ["category_name"]}),
        ("Content", {"fields": ["summary", "content", "image"]}),
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
admin.site.register(Article, ArticleAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
