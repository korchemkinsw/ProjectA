from clientele.models import Individual, Legal
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

class Sim(models.Model):
    iccid = models.CharField(
        max_length=20,
        verbose_name='Номер SIM-карты',
        help_text='Номер SIM-карты',
        blank=True,
        unique=True
    )
    msisdn = models.CharField(
        max_length=11,
        verbose_name='Абонентский номер',
        help_text='Абонентский номер',
        blank=True,
        unique=True
    )
    device = models.ForeignKey(
        Device,
        verbose_name='ППК',
        help_text='ППК',
        null=True,
        on_delete=models.SET_NULL,
        related_name='sim',
    )

    class Meta:
        verbose_name = 'SIM-карта'
        verbose_name_plural = 'SIM-карты'

    def __str__(self):
        return f'{self.device} {self.iccid} {self.msisdn}'

class Card(models.Model):
    ANDROMEDA = 'andromeda'
    RITM = 'ritm'
    NAVIGARD = 'navigard'
    ELDES = 'eldes'
    JABLOTRON = 'jablotron'
    DX = 'dx'
    OTHER ='other'

    NEW = 'новый'
    ACCOUNT = 'пультовой номер'
    CONTRACT = 'договор'
    MONTAGE = 'монтаж'
    CHANGED = 'изменён'
    COMPLETED = 'завершен'

    SYSTEMS = (
        (ANDROMEDA, 'Си-Норд'),
        (RITM, 'Ритм'),
        (NAVIGARD, 'Навигард'),
        (ELDES, 'Eldes'),
        (JABLOTRON, 'Jablotron'),
        (DX, 'DX'),
        (OTHER, 'Прочее оборудование'),
    )

    STATUS_CHOICES = (
        (NEW, 'Новый'),
        (ACCOUNT, 'Пультовой номер'),
        (CONTRACT, 'Договор'),
        (MONTAGE, 'Монтаж'),
        (CHANGED, 'Изменён'),
        (COMPLETED, 'Завершен'),
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='Новый',
        verbose_name='Статус заявки',
    )
    legal = models.ForeignKey(
        Legal,
        verbose_name='Юр.лицо',
        help_text='Юр.лицо',
        on_delete=models.SET_NULL,
        related_name='legal_app',
        blank=True,
        null=True,
    )
    individual = models.ForeignKey(
        Individual,
        verbose_name='Физ.лицо',
        help_text='Физ.лицо',
        on_delete=models.SET_NULL,
        related_name='individ_app',
        blank=True,
        null=True,
    )
    object_name = models.CharField(
        max_length=400,
        verbose_name='Название объекта',
        help_text='Название объекта',
        null=True,
    )
    address = models.CharField(
        max_length=400,
        verbose_name='Адрес',
        help_text='Адрес',
        blank=True,
    )
    transmission = models.CharField(
        max_length=20,
        choices=SYSTEMS,
        default=OTHER,
        verbose_name='СПИ',
    )
    note = models.CharField(
        max_length=200,
        verbose_name='Примечание',
        help_text='Примечание',
        blank=True
    )
    device = models.ForeignKey(
        Device,
        verbose_name='ППК',
        help_text='ППК',
        null=True,
        on_delete=models.SET_NULL,
        related_name='control',
    )
    qteam = models.ForeignKey(
        Responseteam,
        verbose_name='Группа реагирования',
        on_delete=models.SET_NULL,
        related_name='qteam',
        null=True,
        blank=True,
    )
    manager = models.ForeignKey(
        User,
        verbose_name='Ответственный менеджер',
        on_delete=models.SET_NULL,
        related_name='manager',
        null=True,
        blank=True,
    )
    generated = models.DateTimeField(
        'Дата создания',
        null=True,
        blank=True,
        #auto_now_add=True
    )

    class Meta:
        verbose_name = 'Карточка объекта'
        verbose_name_plural = 'Карточки объектов'

    def __str__(self):
        if self.legal:
            return f'{self.device.account} {self.legal} {self.object_name} {self.address}'
        if self.individual:
            return f'{self.device.account} {self.individual} {self.object_name} {self.address}'


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
