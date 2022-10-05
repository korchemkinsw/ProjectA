# Generated by Django 2.2.19 on 2022-10-05 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientele', '0005_contract_filecontract'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'verbose_name': 'Телефон', 'verbose_name_plural': 'Телефоны'},
        ),
        migrations.AddField(
            model_name='contract',
            name='status',
            field=models.CharField(choices=[('новый', 'новый'), ('действующий', 'действующий'), ('приостановлен', 'приостановлен'), ('закрыт', 'закрыт')], default='новый', max_length=15, verbose_name='Статус договора'),
        ),
    ]
