# Generated by Django 2.2.19 on 2022-09-20 10:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clientele', '0002_application_manager'),
        ('object_card', '0001_initial'),
        ('enterprises', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='enginer_pult',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='enginer_pult', to=settings.AUTH_USER_MODEL, verbose_name='Инженер пульта'),
        ),
        migrations.AddField(
            model_name='contract',
            name='contract_holder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='holder', to=settings.AUTH_USER_MODEL, verbose_name='Ответственный от предприятия'),
        ),
        migrations.AddField(
            model_name='contract',
            name='enterprise',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='enterprise', to='enterprises.Enterprise', verbose_name='Охранное предприятие'),
        ),
        migrations.AddField(
            model_name='contract',
            name='qteam',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='qteam', to='enterprises.Responseteam', verbose_name='Группа реагирования'),
        ),
        migrations.AddField(
            model_name='card',
            name='application',
            field=models.ForeignKey(help_text='Объект', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='object', to='clientele.Application', verbose_name='Объект'),
        ),
        migrations.AddField(
            model_name='card',
            name='contract',
            field=models.ForeignKey(help_text='Договор', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contract', to='object_card.Contract', verbose_name='Договор'),
        ),
        migrations.AddField(
            model_name='card',
            name='device',
            field=models.ForeignKey(help_text='ППК', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='control_device', to='object_card.Device', verbose_name='ППК'),
        ),
        migrations.AddField(
            model_name='card',
            name='enginer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='enginer', to=settings.AUTH_USER_MODEL, verbose_name='Ответственный инженер'),
        ),
    ]