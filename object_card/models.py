import os
import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from simple_history.models import HistoricalRecords

from clientele.models import Contact, Contract, Individual, Legal
from enterprises.models import Responseteam

User = get_user_model()

ANDROMEDA = 'Си-Норд'
RITM = 'Ритм'
NAVIGARD = 'Навигард'
ELDES = 'Eldes'
JABLOTRON = 'Jablotron'
DX = 'DX'
OTHER ='Прочее оборудование'
NONE = 'Без оборудования'

SYSTEMS = (
    (ANDROMEDA, 'Си-Норд'),
    (RITM, 'Ритм'),
    (NAVIGARD, 'Навигард'),
    (ELDES, 'Eldes'),
    (JABLOTRON, 'Jablotron'),
    (DX, 'DX'),
    (OTHER, 'Прочее оборудование'),
    (NONE, 'Без оборудования')
)

class Type_device(models.Model):
    transmission = models.CharField(
        max_length=20,
        choices=SYSTEMS,
        verbose_name='СПИ',
    )
    device = models.CharField(
        max_length=30,
        verbose_name='Тип ППК',
        help_text='Тип ППК',
        unique=True
    )
    class Meta:
        verbose_name = 'Тип ППК'
        verbose_name_plural = 'Типы ППК'

    def __str__(self):
        return f'{self.device}'

class Device(models.Model):
    account = models.CharField(
        max_length=8,
        verbose_name='Передаваемый номер',
        help_text='Передаваемый номер',
        unique=True
    )
    device = models.ForeignKey(
        Type_device,
        verbose_name='Тип ППК',
        on_delete=models.SET_NULL,
        related_name='type',
        null=True,
        blank=True,
    )
    note = models.CharField(
        max_length=200,
        verbose_name='Примечание',
        help_text='Примечание',
        blank=True
    )
    none = models.CharField(
        max_length=1,
        verbose_name='--пусто--',
        help_text='--пусто--',
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
        'Дата создания',
        null=True,
        blank=True,
    )
    technican = models.ForeignKey(
        User,
        verbose_name='Техник',
        on_delete=models.SET_NULL,
        related_name='technican',
        null=True,
        blank=True,
    )
    changed_tech = models.DateTimeField(
        'Дата изменения',
        null=True,
        blank=True,
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Оборудование на объекте'
        verbose_name_plural = 'Оборудование на объектах'

    def __str__(self):
        return self.account

class Sim(models.Model):
    SIM1 = 'sim 1'
    SIM2 = 'sim 2'
    REP = 'зам.'
    BLOCK = 'блок'
    SIM_CHOICES = (
        (SIM1, 'sim 1'),
        (SIM2, 'sim 2'),
        (REP, 'зам.'),
        (BLOCK, 'блок')
    )
    part_sim = models.CharField(
        max_length=5,
        choices=SIM_CHOICES,
        blank=True,
        verbose_name='sim #',
    )
    iccid = models.CharField(
        max_length=20,
        verbose_name='Номер SIM-карты',
        help_text='Номер SIM-карты',
        blank=True,
    )
    msisdn = models.CharField(
        max_length=11,
        verbose_name='Абонентский номер',
        help_text='Абонентский номер',
        blank=True,
    )
    device = models.ForeignKey(
        Device,
        verbose_name='ППК',
        help_text='ППК',
        on_delete=models.CASCADE,
        related_name='sim',
    )

    def generate_path(instance, filename):
        return os.path.join('object_card', str(instance.device.account)+"_sim", filename)

    image = models.ImageField(verbose_name='Фото sim-карты', upload_to=generate_path, blank=True, null=True)
    
    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(Sim,self).delete(*args,**kwargs)
        storage.delete(path)
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'SIM-карта'
        verbose_name_plural = 'SIM-карты'

    def __str__(self):
        return f'{self.device} {self.iccid} {self.msisdn}'

class Card(models.Model):
    NEW = 'новый'
    ACCOUNT = 'пультовой номер'
    CONTRACT = 'договор'
    RESPONSE = 'реагирование'
    MONTAGE = 'монтаж'
    CHANGED = 'изменён'
    COMPLETED = 'завершен'

    STATUS_CHOICES = (
        (NEW, 'Новый'),
        (ACCOUNT, 'Пультовой номер'),
        (CONTRACT, 'Договор'),
        (RESPONSE, 'Реагирование'),
        (MONTAGE, 'Монтаж'),
        (CHANGED, 'Изменён'),
        (COMPLETED, 'Завершен'),
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='Новый',
        verbose_name='Статус объекта',
    )
    object_key = models.CharField(
        max_length=20,
        verbose_name='Ключ объекта',
        help_text='Ключ объекта',
        blank=True,
        unique=True
    )
    legal = models.ForeignKey(
        Legal,
        verbose_name='Юр.лицо',
        help_text='Юр.лицо',
        on_delete=models.SET_NULL,
        related_name='legal_card',
        blank=True,
        null=True,
    )
    individual = models.ForeignKey(
        Individual,
        verbose_name='Физ.лицо',
        help_text='Физ.лицо',
        on_delete=models.SET_NULL,
        related_name='individ_card',
        blank=True,
        null=True,
    )
    object_name = models.CharField(
        max_length=400,
        verbose_name='Название объекта',
        help_text='Название объекта',
    )
    phone = models.CharField(
        max_length=50,
        verbose_name='Телефон на объекте',
        help_text='Телефон на объекте',
        blank=True,
    )
    address = models.CharField(
        max_length=400,
        verbose_name='Адрес',
        help_text='Адрес',
    )
    transmission = models.CharField(
        max_length=20,
        choices=SYSTEMS,
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
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='control',
    )
    contract = models.ForeignKey(
        Contract,
        verbose_name='Договор',
        help_text='Договор',
        on_delete=models.SET_NULL,
        related_name='contract',
        blank=True,
        null=True,
    )
    qteam = models.ForeignKey(
        Responseteam,
        verbose_name='Группа реагирования',
        on_delete=models.SET_NULL,
        related_name='responseteam',
        null=True,
        blank=True,
    )
    qnote = models.CharField(
        max_length=200,
        verbose_name='информация для ГБР',
        help_text='информация для ГБР',
        blank=True
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
    )
    director = models.ForeignKey(
        User,
        verbose_name='Ответственный за договор',
        on_delete=models.SET_NULL,
        related_name='director',
        null=True,
        blank=True,
    )
    changed = models.DateTimeField(
        'Дата изменения',
        null=True,
        blank=True,
    )
    none = models.CharField(
        max_length=1,
        verbose_name='--пусто--',
        help_text='--пусто--',
        blank=True,
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Карточка объекта'
        verbose_name_plural = 'Карточки объектов'

    def __str__(self):
        if self.legal:
            return f'{self.legal} {self.object_name} {self.address}'
        if self.individual:
            return f'{self.individual} {self.object_name} {self.address}'

class GPS(models.Model):
    card = models.ForeignKey(
        Card,
        verbose_name='Объект',
        help_text='Объект',
        null=True,
        on_delete=models.CASCADE,
        related_name='card_gps',
    )
    gps = models.CharField(
        max_length=19,
        verbose_name='координаты GPS',
        help_text='координаты GPS',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'координаты GPS'
        verbose_name_plural = 'координаты GPS'

    def __str__(self):
        return f'{self.gps} {self.card.address[:50]}...'

    def clean(self):
        if not re.fullmatch(r'^[5-6][0-9][.][0-9]{6}[\s][2-4][0-9][.][0-9]{6}', str(self.gps)):
            raise ValidationError(
                {'gps': 'Координаты не верны'}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

class Qteam(models.Model):
    BASIC = 'основная'
    RESERVE = 'резервная'
    TYPE = (
        (BASIC, 'основная'),
        (RESERVE, 'резервная'),
    )
    card = models.ForeignKey(
        Card,
        verbose_name='Объект',
        help_text='Объект',
        null=True,
        on_delete=models.CASCADE,
        related_name='card_qtem',
    )
    type = models.CharField(
        max_length=15,
        choices=TYPE,
        default='основная',
        verbose_name='тип группы',
    )
    qteam = models.ForeignKey(
        Responseteam,
        verbose_name='Группа реагирования',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Группа реагирования'
        verbose_name_plural = 'Группы реагирования'

    def __str__(self):
        return f'{self.card} {self.type} {self.qteam}'

class Partition(models.Model):
    device = models.ForeignKey(
        Device,
        verbose_name='ППК',
        help_text='ППК',
        null=True,
        on_delete=models.CASCADE,
        related_name='partition',
    )
    number = models.PositiveIntegerField(
        verbose_name='№',
        help_text='№',
    )
    name = models.CharField(
        max_length=20,
        verbose_name='Название раздела',
        help_text='Название раздела',
        blank=True
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        return f'{self.number} {self.name}'

class Zone(models.Model):
    device = models.ForeignKey(
        Device,
        verbose_name='ППК',
        help_text='ППК',
        null=True,
        on_delete=models.CASCADE,
        related_name='zones',
    )
    partition = models.ForeignKey(
        Partition,
        verbose_name='Раздел',
        help_text='Раздел',
        null=True,
        on_delete=models.CASCADE,
    )
    number = models.PositiveIntegerField(
        verbose_name='№',
        help_text='№',
    )
    name = models.CharField(
        max_length=20,
        verbose_name='Название зоны',
        help_text='Название зоны',
        blank=True
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Зона'
        verbose_name_plural = 'Зоны'

    def __str__(self):
        return f'{self.device} | {self.partition} | {self.number} {self.name}'

class Person(models.Model):
    APPLICATION = (
        ('MyAlarm', 'MyAlarm'),
        ('GeoRitm', 'GeoRitm'),
        ('PhoenixMK', 'PhoenixMK'),
    )
    card = models.ForeignKey(
        Card,
        verbose_name='Объект',
        help_text='Объект',
        null=True,
        on_delete=models.CASCADE,
        related_name='card_person',
    )
    number = models.PositiveIntegerField(
        verbose_name='№',
        help_text='№',
    )
    person = models.ForeignKey(
        Contact,
        verbose_name='Ответственное лицо',
        on_delete=models.CASCADE,
    )
    note = models.CharField(
        max_length=50,
        verbose_name='Примечание',
        blank=True,
    )
    application = models.CharField(
        max_length=9,
        choices=APPLICATION,
        blank=True,
        verbose_name='Приложение',
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Ответственное лицо'
        verbose_name_plural = 'Ответственные лица'

    def __str__(self):
        return f'{self.card} {self.person}'

class CardPhoto(models.Model):
    card = models.ForeignKey(
        Card,
        verbose_name='Объект',
        help_text='Объект',
        null=True,
        on_delete=models.CASCADE,
        related_name='card_photo',
    )
    title = models.CharField(
        max_length=30,
        verbose_name='Описание',
        help_text='Описание',
    )
    
    def generate_path(instance, filename):
        object_name=str(instance.card.object_name)
        for simb, new in (" ", "-"), ("/", "-"), ('"', ""):
            object_name=object_name.replace(simb, new)
        return os.path.join('object_card', str(instance.card.device.account)+'_'+object_name, filename)

    image = models.ImageField(verbose_name='Фотография объекта', upload_to=generate_path, blank=True)

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(CardPhoto,self).delete(*args,**kwargs)
        storage.delete(path)

    class Meta:
        verbose_name = 'Фотография объекта'
        verbose_name_plural = 'Фотографии объектов'
