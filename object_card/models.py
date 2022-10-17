import os
from enum import unique

from clientele.models import Contract, Individual, Legal
from django.contrib.auth import get_user_model
from django.db import models
from enterprises.models import Responseteam

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

    class Meta:
        verbose_name = 'Оборудование на объекте'
        verbose_name_plural = 'Оборудование на объектах'

    def __str__(self):
        return self.account

class Sim(models.Model):
    iccid = models.CharField(
        max_length=20,
        verbose_name='Номер SIM-карты',
        help_text='Номер SIM-карты',
        blank=True,
        #unique=True
    )
    msisdn = models.CharField(
        max_length=11,
        verbose_name='Абонентский номер',
        help_text='Абонентский номер',
        blank=True,
        #unique=True
    )
    device = models.ForeignKey(
        Device,
        verbose_name='ППК',
        help_text='ППК',
        null=True,
        on_delete=models.CASCADE,
        related_name='sim',
    )
    
    class Meta:
        verbose_name = 'SIM-карта'
        verbose_name_plural = 'SIM-карты'

    def __str__(self):
        return f'{self.device} {self.iccid} {self.msisdn}'

class ImageSim(models.Model):
    SIM1 = 'sim 1'
    SIM2 = 'sim 2'
    SIM_CHOICES = (
        (SIM1, 'sim 1'),
        (SIM2, 'sim 2'),
    )
    device = models.ForeignKey(
        Device,
        verbose_name='ППК',
        help_text='ППК',
        null=True,
        on_delete=models.CASCADE,
        related_name='image_sim',
    )
    part_sim = models.CharField(
        max_length=5,
        choices=SIM_CHOICES,
        #unique=True,
        verbose_name='sim #',
    )
 
    def generate_path(instance, filename):
        return os.path.join('object_card', str(instance.device.account)+"/sim", filename)

    image = models.ImageField(verbose_name='Фото sim-карты', upload_to=generate_path, blank=True)

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(ImageSim,self).delete(*args,**kwargs)
        storage.delete(path)

    class Meta:
        verbose_name = 'Фотография sim-карты'
        verbose_name_plural = 'Фотографии sim-карт'

    def __str__(self):
        return f'{self.device.account} {self.part_sim} {self.image}'


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
        null=True,
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
        blank=True,
    )
    width = models.CharField(
        max_length=9,
        verbose_name='широта',
        help_text='широта',
        blank=True,
    )
    longitude = models.CharField(
        max_length=9,
        verbose_name='долгота',
        help_text='долгота',
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
        related_name='qteam',
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

    class Meta:
        verbose_name = 'Карточка объекта'
        verbose_name_plural = 'Карточки объектов'

    def __str__(self):
        if self.legal:
            return f'{self.legal} {self.object_name} {self.address}'
        if self.individual:
            return f'{self.individual} {self.object_name} {self.address}'


class Partition(models.Model):
    device = models.ForeignKey(
        Device,
        verbose_name='ППК',
        help_text='ППК',
        null=True,
        on_delete=models.CASCADE,
        related_name='partition',
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
        return f'{self.device} | {self.partition} | {self.number} {self.name}'

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
        return os.path.join('object_card', str(instance.card.device.account)+'_'+str(instance.card.object_name), filename)

    image = models.ImageField(verbose_name='Фотография объекта', upload_to=generate_path, blank=True)

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(CardPhoto,self).delete(*args,**kwargs)
        storage.delete(path)

    class Meta:
        verbose_name = 'Фотография объекта'
        verbose_name_plural = 'Фотографии объектов'
