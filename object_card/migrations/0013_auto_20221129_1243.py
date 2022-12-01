# Generated by Django 2.2.19 on 2022-11-29 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('object_card', '0012_historicalperson_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalperson',
            name='note',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Примечание'),
        ),
        migrations.AlterField(
            model_name='historicalperson',
            name='person',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='clientele.Responsible', verbose_name='Ответственное лицо'),
        ),
        migrations.AlterField(
            model_name='person',
            name='note',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Примечание'),
        ),
        migrations.AlterField(
            model_name='person',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientele.Responsible', verbose_name='Ответственное лицо'),
        ),
    ]
