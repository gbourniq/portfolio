# Generated by Django 2.2.4 on 2019-08-16 22:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20190816_2237'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='subcat_name',
            new_name='subcategory_name',
        ),
    ]
