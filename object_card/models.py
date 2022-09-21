from email.mime import application

from clientele.models import Application
from django.contrib.auth import get_user_model
from django.db import models
from enterprises.models import Enterprise, Responseteam

User = get_user_model()


class Device(models.Model):
    account = models.CharField(
        max_length=8,
        verbose_name='Номер объекта',
        help_text='Номер объекта',
        blank=True
    )
    device = models.CharField(
        max_length=20,
        verbose_name='Прибор',
        help_text='Прибор',
        blank=True
    )
    sim_first = models.CharField(
        max_length=24,
        verbose_name='Первая сим',
        help_text='Первая сим',
        blank=True
    )
    sim_two = models.CharField(
        max_length=24,
        verbose_name='Вторая сим',
        help_text='Вторая сим',
        blank=True
    )
    application = models.ForeignKey(
        Application,
        verbose_name='Объект',
        help_text='Объект',
        null=True,
        on_delete=models.SET_NULL,
        related_name='controldev',
    )
    enginer_pult = models.ForeignKey(
        User,
        verbose_name='Инженер пульта',
        on_delete=models.SET_NULL,
        related_name='enginer_pult',
        null=True,
        blank=True,
    )
    changed_pult = models.DateTimeField(
        'Дата изменения',
        null=True,
        blank=True,
        #auto_now_add=True
    )

    class Meta:
        verbose_name = 'Оборудование на объекте'
        verbose_name_plural = 'Оборудование на объектах'

    def __str__(self):
        return f'{self.account}'

class Contract(models.Model):
    enterprise = models.ForeignKey(
        Enterprise,
        verbose_name='Охранное предприятие',
        on_delete=models.SET_NULL,
        related_name='enterprise',
        null=True,
        blank=True,
    )
    number = models.CharField(
        max_length=8,
        verbose_name='Номер договора',
        help_text='Номер договора',
        blank=True
    )
    application = models.ForeignKey(
        Application,
        verbose_name='Объект',
        help_text='Объект',
        null=True,
        on_delete=models.SET_NULL,
        related_name='contract',
    )
    qteam = models.ForeignKey(
        Responseteam,
        verbose_name='Группа реагирования',
        on_delete=models.SET_NULL,
        related_name='qteam',
        null=True,
        blank=True,
    )
    contract_holder = models.ForeignKey(
        User,
        verbose_name='Ответственный от предприятия',
        on_delete=models.SET_NULL,
        related_name='holder',
        null=True,
        blank=True,
    )
    changed_ent = models.DateTimeField(
        'Дата изменения',
        null=True,
        blank=True,
        #auto_now_add=True
    )

    class Meta:
        verbose_name = 'Реагирование'
        verbose_name_plural = 'Реагирование'

    def __str__(self):
        return f'{self.enterprise} {self.qteam}'

class Card(models.Model):
    device = models.ForeignKey(
        Device,
        verbose_name='ППК',
        help_text='ППК',
        null=True,
        on_delete=models.SET_NULL,
        related_name='control',
    )
    application = models.ForeignKey(
        Application,
        verbose_name='Объект',
        help_text='Объект',
        null=True,
        on_delete=models.SET_NULL,
        related_name='object',
    )
    contract = models.ForeignKey(
        Contract,
        verbose_name='Договор',
        help_text='Договор',
        null=True,
        on_delete=models.SET_NULL,
        related_name='contr',
    )

    enginer = models.ForeignKey(
        User,
        verbose_name='Ответственный инженер',
        null=True,
        on_delete=models.SET_NULL,
        related_name='enginer',
        blank=True,
    )
    generated = models.DateTimeField(
        'Дата заполнения',
        null=True,
        blank=True,
        #auto_now_add=True
    )

    class Meta:
        verbose_name = 'Карточка объекта'
        verbose_name_plural = 'Карточки объектов'

    def __str__(self):
        return f'{self.application}{self.enginer} {self.generated}'

class Partition(models.Model):
    device = models.ForeignKey(
        Device,
        verbose_name='Оборудование',
        help_text='Оборудование',
        null=True,
        on_delete=models.SET_NULL,
        related_name='card',
    )
    number = models.IntegerField(
        verbose_name='Номер раздела',
        help_text='Номер раздела',
    )
    name = models.CharField(
        max_length=20,
        verbose_name='Название раздела',
        help_text='Название раздела',
        blank=True
    )

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        return f'{self.number} {self.name}'

class Zone(models.Model):
    partition = models.ForeignKey(
        Partition,
        verbose_name='Раздел',
        help_text='Раздел',
        null=True,
        on_delete=models.SET_NULL,
        related_name='partition',
    )
    number = models.IntegerField(
        verbose_name='Номер зоны',
        help_text='Номер зоны',
    )
    name = models.CharField(
        max_length=20,
        verbose_name='Название зоны',
        help_text='Название зоны',
        blank=True
    )

    class Meta:
        verbose_name = 'Зона'
        verbose_name_plural = 'Зоны'

    def __str__(self):
        return f'{self.card} | {self.number} {self.name}'
