# Generated by Django 2.2.4 on 2019-12-28 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="image",
            field=models.ImageField(upload_to="main/static/images/"),
        ),
        migrations.AlterField(
            model_name="category",
            name="image",
            field=models.ImageField(upload_to="main/static/images/"),
        ),
        migrations.AlterField(
            model_name="subcategory",
            name="image",
            field=models.ImageField(upload_to="main/static/images/"),
        ),
    ]