# Generated by Django 2.2.9 on 2023-02-15 11:12

from django.db import migrations, models
import django.db.models.deletion
import enterprises.models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprises', '0002_security_worker'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weapon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(choices=[('ИЖ-71', 'ИЖ-71')], default='ИЖ-71', max_length=11, verbose_name='Модель оружия')),
                ('caliber', models.CharField(choices=[('9 мм', '9 мм')], default='9 мм', max_length=5, verbose_name='Калибр')),
                ('series', models.CharField(choices=[('ВЕТ', 'ВЕТ')], max_length=3, verbose_name='Серия')),
                ('number', models.CharField(max_length=4, verbose_name='Номер')),
            ],
            options={
                'verbose_name': 'Оружие',
                'verbose_name_plural': 'Оружие',
            },
        ),
        migrations.AlterModelOptions(
            name='security',
            options={'verbose_name': 'Охранник', 'verbose_name_plural': 'Охранники'},
        ),
        migrations.AddField(
            model_name='security',
            name='note',
            field=models.CharField(blank=True, max_length=200, verbose_name='Примечание'),
        ),
        migrations.AddField(
            model_name='security',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=enterprises.models.Security.generate_path, verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='security',
            name='category',
            field=models.CharField(choices=[('4 разряд', '4 разряд'), ('5 разряд', '5 разряд'), ('6 разряд', '6 разряд')], max_length=8, verbose_name='разряд'),
        ),
        migrations.AlterField(
            model_name='security',
            name='issue',
            field=models.DateField(verbose_name='Дата выдачи'),
        ),
        migrations.AlterField(
            model_name='security',
            name='prolonged',
            field=models.DateField(blank=True, verbose_name='Дата продления'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Фамилия Имя Отчество'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enterprises.Position', verbose_name='Должность'),
        ),
        migrations.CreateModel(
            name='WeaponsPermit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series', models.CharField(choices=[('РСЛа', 'РСЛа')], default='РСЛа', max_length=4, verbose_name='Серия')),
                ('number', models.CharField(max_length=7, verbose_name='Номер')),
                ('issue', models.DateField(verbose_name='Дата выдачи')),
                ('enterprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enterprises.Enterprise', verbose_name='Предприятие')),
                ('security', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enterprises.Security', verbose_name='Охранник')),
                ('weapon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enterprises.Weapon', verbose_name='Оружие')),
            ],
            options={
                'verbose_name': 'Разрешение на хранение и ношение оружия',
                'verbose_name_plural': 'Разрешения на хранение и ношение оружия',
            },
        ),
    ]
