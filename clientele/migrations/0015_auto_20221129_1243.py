# Generated by Django 2.2.19 on 2022-11-29 12:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientele', '0014_auto_20221129_1136'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'verbose_name': 'Контакт', 'verbose_name_plural': 'Книга контактов'},
        ),
        migrations.AlterModelOptions(
            name='responsible',
            options={'verbose_name': 'Лицо', 'verbose_name_plural': 'Лица'},
        ),
        migrations.AlterField(
            model_name='filecontract',
            name='generated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 29, 12, 43, 55, 225321), null=True, verbose_name='Дата создания'),
        ),
    ]
