# Generated by Django 2.2.19 on 2022-03-19 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filesorder',
            name='docum',
        ),
        migrations.AddField(
            model_name='filesorder',
            name='file',
            field=models.FileField(default='none', upload_to='', verbose_name='Файлы'),
            preserve_default=False,
        ),
    ]
