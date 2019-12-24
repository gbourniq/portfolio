# Generated by Django 2.2.4 on 2019-08-16 23:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_auto_20190816_2239"),
    ]

    operations = [
        migrations.CreateModel(
            name="Article",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("article_name", models.CharField(max_length=200)),
                ("summary", models.CharField(max_length=200)),
                ("content", models.TextField()),
                ("image", models.ImageField(upload_to="images/")),
                (
                    "date_published",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="date published",
                    ),
                ),
                ("article_slug", models.CharField(default=1, max_length=200)),
            ],
            options={"verbose_name_plural": "Articles",},
        ),
        migrations.DeleteModel(name="Card",),
        migrations.AlterField(
            model_name="subcategory",
            name="category_name",
            field=models.ForeignKey(
                default=1,
                on_delete="SET_DEFAULT",
                to="main.Category",
                verbose_name="Category",
            ),
        ),
        migrations.AddField(
            model_name="article",
            name="subcategory_name",
            field=models.ForeignKey(
                default=1,
                on_delete="SET_DEFAULT",
                to="main.SubCategory",
                verbose_name="SubCategory",
            ),
        ),
    ]
