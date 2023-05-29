# Generated by Django 2.2.9 on 2023-02-17 11:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprises', '0004_auto_20230215_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='weapon',
            name='release',
            field=models.IntegerField(default=2000, max_length=4, validators=[django.core.validators.MinValueValidator(1990), django.core.validators.MaxValueValidator(2023)], verbose_name='Год выпуска'),
            preserve_default=False,
        ),
    ]