# Generated by Django 2.2.9 on 2023-04-19 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientele', '0001_initial'),
        ('security_post', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guardobject',
            name='enterprise',
        ),
        migrations.RemoveField(
            model_name='guardobject',
            name='individual',
        ),
        migrations.RemoveField(
            model_name='guardobject',
            name='legal',
        ),
        migrations.AddField(
            model_name='guardobject',
            name='contract',
            field=models.ForeignKey(help_text='Договор', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contract_post', to='clientele.Contract', verbose_name='Договор'),
        ),
        migrations.AlterField(
            model_name='guardobject',
            name='qteam',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_post', to='enterprises.Responseteam', verbose_name='Группа реагирования'),
        ),
    ]