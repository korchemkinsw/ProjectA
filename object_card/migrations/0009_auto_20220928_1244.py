# Generated by Django 2.2.19 on 2022-09-28 12:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('object_card', '0008_auto_20220928_0956'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='chnged',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата изменения'),
        ),
        migrations.AddField(
            model_name='card',
            name='director',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='director', to=settings.AUTH_USER_MODEL, verbose_name='Ответственный за договор'),
        ),
        migrations.AddField(
            model_name='device',
            name='changed_tech',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата изменения'),
        ),
        migrations.AddField(
            model_name='device',
            name='note',
            field=models.CharField(blank=True, help_text='Примечание', max_length=200, verbose_name='Примечание'),
        ),
        migrations.AddField(
            model_name='device',
            name='technican',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='technican', to=settings.AUTH_USER_MODEL, verbose_name='Техник'),
        ),
        migrations.AddField(
            model_name='zone',
            name='device',
            field=models.ForeignKey(help_text='ППК', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='zones', to='object_card.Device', verbose_name='ППК'),
        ),
        migrations.AlterField(
            model_name='device',
            name='changed_pult',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='zone',
            name='partition',
            field=models.ForeignKey(help_text='Раздел', null=True, on_delete=django.db.models.deletion.SET_NULL, to='object_card.Partition', verbose_name='Раздел'),
        ),
    ]