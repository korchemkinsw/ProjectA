# Generated by Django 2.2.19 on 2022-06-07 07:27

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0009_remove_order_contractor'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contractorsorder',
            options={},
        ),
        migrations.AlterModelOptions(
            name='fileorder',
            options={'verbose_name': 'Файл приказа', 'verbose_name_plural': 'Файл приказа'},
        ),
        migrations.RemoveField(
            model_name='fileorder',
            name='order',
        ),
        migrations.AddField(
            model_name='order',
            name='contractor',
            field=models.ManyToManyField(blank=True, related_name='contractors_order', through='orders.ContractorsOrder', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='fileorder',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='perday',
            field=models.DateField(default=datetime.date(2022, 6, 7), verbose_name='Выполнить в'),
        ),
        migrations.CreateModel(
            name='FilesOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='orders.FileOrder', verbose_name='Файлы приказа')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='files', to='orders.Order', verbose_name='Приказ')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='order',
            field=models.ManyToManyField(blank=True, related_name='files_order', through='orders.FilesOrder', to='orders.FileOrder', verbose_name='Файлы приказа'),
        ),
    ]
