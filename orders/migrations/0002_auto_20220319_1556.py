# Generated by Django 2.2.19 on 2022-03-19 15:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('enterprises', '0002_enterprise_bigboss'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='contractor',
            field=models.ManyToManyField(related_name='contractors_order', through='orders.ContractorsOrder', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='firm',
            field=models.ForeignKey(help_text='Предприятие', on_delete=django.db.models.deletion.CASCADE, related_name='firm', to='enterprises.Enterprise', verbose_name='Предприятие'),
        ),
        migrations.AddField(
            model_name='order',
            name='lastuser',
            field=models.ForeignKey(help_text='Последний пользователь', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lastuser', to=settings.AUTH_USER_MODEL, verbose_name='Последний пользователь'),
        ),
        migrations.AddField(
            model_name='filesorder',
            name='docum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.FileOrder'),
        ),
        migrations.AddField(
            model_name='filesorder',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.Order', verbose_name='Приказ'),
        ),
        migrations.AddField(
            model_name='contractorsorder',
            name='contractor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Исполнители'),
        ),
        migrations.AddField(
            model_name='contractorsorder',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.Order', verbose_name='Приказ'),
        ),
    ]
