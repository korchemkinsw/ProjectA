# Generated by Django 2.2.19 on 2022-08-09 11:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20220711_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='perday',
            field=models.DateField(default=datetime.date(2022, 8, 9), verbose_name='Выполнить в'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('новый', 'Новый'), ('в работе', 'В работе'), ('завершен', 'Завершен'), ('отклонен', 'Отклонен'), ('Просрочен!', 'Просрочен!')], default='Новый', max_length=10, verbose_name='Статус приказа'),
        ),
    ]