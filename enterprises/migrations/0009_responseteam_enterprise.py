# Generated by Django 2.2.9 on 2023-04-19 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('enterprises', '0008_auto_20230419_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='responseteam',
            name='enterprise',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='enterprises.Enterprise', verbose_name='Предприятие'),
        ),
    ]
