from django.contrib import admin
from .models import Article, SubCategory, Category
from tinymce.widgets import TinyMCE
from django.db import models


class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title/date", {"fields":["article_name", "date_published"]}),
        ("URL", {"fields":["article_slug"]}),
        ("Parent Element", {"fields":["subcategory_name"]}),
        ("Content", {"fields":["summary", "content", "image"]})
    ]
    # Overwrite properties for TextFields only
    formfield_overrides = {
    	models.TextField: {'widget':TinyMCE()},
    }

class SubCategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title", {"fields":["subcategory_name", "subcategory_slug"]}),
        ("Parent Element", {"fields":["category_name"]}),
        ("Content", {"fields":["summary", "content", "image"]})
    ]
    # Overwrite properties for TextFields only
    formfield_overrides = {
    	models.TextField: {'widget':TinyMCE()},
    }
    
# Register your models here.
admin.site.register(Article, ArticleAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Category)