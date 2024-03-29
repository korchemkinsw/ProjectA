# Generated by Django 2.2.9 on 2023-02-15 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('enterprises', '0003_auto_20230215_1112'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series', models.CharField(default='78', max_length=2, verbose_name='Серия')),
                ('number', models.CharField(max_length=13, verbose_name='Номер')),
                ('type', models.CharField(choices=[('основной', 'основное'), ('совместитель', 'совместитель')], default='основное', max_length=12, verbose_name='Тип')),
                ('issue', models.DateField(verbose_name='Дата выдачи')),
            ],
            options={
                'verbose_name': 'Личная карточка охранника',
                'verbose_name_plural': 'Личные карточки охранников',
            },
        ),
        migrations.AlterField(
            model_name='enterprise',
            name='bigboss',
            field=models.ForeignKey(blank=True, help_text='Ген. директор', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bigboss', to='enterprises.Worker', verbose_name='Ген. директор'),
        ),
        migrations.DeleteModel(
            name='Staffer',
        ),
        migrations.AddField(
            model_name='personalcard',
            name='enterprise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enterprises.Enterprise', verbose_name='Предприятие'),
        ),
        migrations.AddField(
            model_name='personalcard',
            name='security',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enterprises.Security', verbose_name='Охранник'),
        ),
    ]
