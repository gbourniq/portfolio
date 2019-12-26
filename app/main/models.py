from django.db import models
from django.utils import timezone

UPLOADS_FOLDER_PATH = "main/static/uploaded_images/"


# Create your models here.\
class Category(models.Model):
    category_name = models.CharField(max_length=200)
    summary = models.TextField()
    image = models.ImageField(upload_to=UPLOADS_FOLDER_PATH)
    category_slug = models.CharField(max_length=200, default=1)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    subcategory_name = models.CharField(max_length=200)
    summary = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to=UPLOADS_FOLDER_PATH)
    subcategory_slug = models.CharField(max_length=200, default=1)
    category_name = models.ForeignKey(
        Category, default=1, verbose_name="Category", on_delete="SET_DEFAULT"
    )

    class Meta:
        verbose_name_plural = "Sub Categories"

    def __str__(self):
        return self.subcategory_name


class Article(models.Model):
    article_name = models.CharField(max_length=200)
    summary = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to=UPLOADS_FOLDER_PATH)
    date_published = models.DateTimeField(
        "date published", default=timezone.now
    )
    article_slug = models.CharField(max_length=200, default=1)
    subcategory_name = models.ForeignKey(
        SubCategory,
        default=1,
        verbose_name="SubCategory",
        on_delete="SET_DEFAULT",
    )

    class Meta:
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.article_name
