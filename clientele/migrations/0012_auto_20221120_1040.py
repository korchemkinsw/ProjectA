# Generated by Django 2.2.19 on 2022-11-20 10:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientele', '0011_auto_20221106_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filecontract',
            name='generated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 20, 10, 40, 11, 448609), null=True, verbose_name='Дата создания'),
        ),
    ]
