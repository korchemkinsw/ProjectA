# Generated by Django 2.2.19 on 2022-10-24 12:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientele', '0009_auto_20221020_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filecontract',
            name='generated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 24, 12, 26, 48, 888035), null=True, verbose_name='Дата создания'),
        ),
    ]