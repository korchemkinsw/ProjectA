# Generated by Django 2.2.9 on 2023-02-14 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('object_card', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='address',
            field=models.CharField(help_text='Адрес', max_length=400, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='card',
            name='object_name',
            field=models.CharField(help_text='Название объекта', max_length=400, verbose_name='Название объекта'),
        ),
        migrations.AlterField(
            model_name='card',
            name='status',
            field=models.CharField(choices=[('новый', 'Новый'), ('пультовой номер', 'Пультовой номер'), ('договор', 'Договор'), ('реагирование', 'Реагирование'), ('монтаж', 'Монтаж'), ('изменён', 'Изменён'), ('завершен', 'Завершен')], default='Новый', max_length=15, verbose_name='Статус объекта'),
        ),
        migrations.AlterField(
            model_name='card',
            name='transmission',
            field=models.CharField(choices=[('Си-Норд', 'Си-Норд'), ('Ритм', 'Ритм'), ('Навигард', 'Навигард'), ('Eldes', 'Eldes'), ('Jablotron', 'Jablotron'), ('DX', 'DX'), ('Прочее оборудование', 'Прочее оборудование'), ('Без оборудования', 'Без оборудования')], max_length=20, verbose_name='СПИ'),
        ),
        migrations.AlterField(
            model_name='device',
            name='account',
            field=models.CharField(help_text='Передаваемый номер', max_length=8, unique=True, verbose_name='Передаваемый номер'),
        ),
        migrations.AlterField(
            model_name='historicalcard',
            name='address',
            field=models.CharField(help_text='Адрес', max_length=400, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='historicalcard',
            name='object_name',
            field=models.CharField(help_text='Название объекта', max_length=400, verbose_name='Название объекта'),
        ),
        migrations.AlterField(
            model_name='historicalcard',
            name='status',
            field=models.CharField(choices=[('новый', 'Новый'), ('пультовой номер', 'Пультовой номер'), ('договор', 'Договор'), ('реагирование', 'Реагирование'), ('монтаж', 'Монтаж'), ('изменён', 'Изменён'), ('завершен', 'Завершен')], default='Новый', max_length=15, verbose_name='Статус объекта'),
        ),
        migrations.AlterField(
            model_name='historicalcard',
            name='transmission',
            field=models.CharField(choices=[('Си-Норд', 'Си-Норд'), ('Ритм', 'Ритм'), ('Навигард', 'Навигард'), ('Eldes', 'Eldes'), ('Jablotron', 'Jablotron'), ('DX', 'DX'), ('Прочее оборудование', 'Прочее оборудование'), ('Без оборудования', 'Без оборудования')], max_length=20, verbose_name='СПИ'),
        ),
        migrations.AlterField(
            model_name='historicaldevice',
            name='account',
            field=models.CharField(db_index=True, help_text='Передаваемый номер', max_length=8, verbose_name='Передаваемый номер'),
        ),
        migrations.AlterField(
            model_name='type_device',
            name='device',
            field=models.CharField(help_text='Тип ППК', max_length=30, unique=True, verbose_name='Тип ППК'),
        ),
        migrations.AlterField(
            model_name='type_device',
            name='transmission',
            field=models.CharField(choices=[('Си-Норд', 'Си-Норд'), ('Ритм', 'Ритм'), ('Навигард', 'Навигард'), ('Eldes', 'Eldes'), ('Jablotron', 'Jablotron'), ('DX', 'DX'), ('Прочее оборудование', 'Прочее оборудование'), ('Без оборудования', 'Без оборудования')], max_length=20, verbose_name='СПИ'),
        ),
    ]