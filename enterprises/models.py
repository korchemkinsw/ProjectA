import datetime as dt
import os
import re

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify

from Project_A.settings import (CALIBER, MODEL, PERMIT_SERIES,
                                SECURITY_CATEGORY, SECURITY_STATUS, SERIES,
                                TYPES, WEAPONMIN)


class Position(models.Model):
    post = models.CharField(
        max_length=70,
        verbose_name='Наименование должности',
        help_text='Наименование должности',
        unique=True,
    )

    class Meta:
        verbose_name = 'Наименование должности'
        verbose_name_plural = 'Наименования должностей'

    def __str__(self):
        return self.post

class Weapon(models.Model):
    model = models.CharField(
        max_length=11,
        choices=MODEL,
        verbose_name='Модель оружия',
        default='ИЖ-71',
    )
    caliber = models.CharField(
        max_length=5,
        choices=CALIBER,
        verbose_name='Калибр',
        default='9 мм',
    )
    series = models.CharField(
        max_length=3,
        verbose_name='Серия',
        choices=SERIES,
    )
    number = models.CharField(
        verbose_name='Номер',
        max_length=4,
    )
    release = models.IntegerField(
        verbose_name='Год выпуска',
        max_length=4,
        default=WEAPONMIN,
        validators=[
            MinValueValidator(WEAPONMIN),
            MaxValueValidator(int(dt.datetime.today().year))
            ],
    )

    class Meta:
        verbose_name = 'Оружие'
        verbose_name_plural = 'Оружие'
    
    def __str__(self):
        return f'{self.model} {self.caliber} {self.series}№{self.number}'

    def clean(self):
        if not re.fullmatch(r'^\d{4}', str(self.number)):
            raise ValidationError(
                {'number': 'Четыре цифры номера'}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

class Worker(models.Model):
    name = models.CharField(
        verbose_name='Фамилия Имя Отчество',
        max_length=150,
    )
    post = models.ForeignKey(
        Position,
        verbose_name='Должность',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
    
    def __str__(self):
        return f'{self.name}: {self.post}'

    def clean(self):
        if not re.fullmatch(r'^[А-ЯЁ][а-яё]+[\S]+[\s][А-ЯЁ][а-яё]+[\s][А-ЯЁ][\D]+', str(self.name)):
            raise ValidationError(
                {'name': 'Фамилия Имя Отчество'}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

class Security(models.Model):
    security = models.ForeignKey(
        Worker,
        verbose_name='Охранник',
        on_delete=models.CASCADE,
        related_name='worker',
    )
    epp = models.DateField(
        verbose_name='ЕПП',
        null=True,
        blank=True,
    )
    medical = models.DateField(
        verbose_name='Медицина',
        null=True,
        blank=True,
    )
    category = models.CharField(
        max_length=8,
        choices=SECURITY_CATEGORY,
        verbose_name='разряд',
    )
    id_number = models.CharField(
        max_length=11,
        verbose_name='Серия и номер удостоверения',
        unique=True
    )
    issue = models.DateField(
        verbose_name='Дата выдачи',
    )
    prolonged = models.DateField(
        verbose_name='Дата продления',
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=11,
        choices=SECURITY_STATUS,
        verbose_name='Статус удостоверения',
        default='действующий',
    )
    note = models.CharField(
        max_length=200,
        verbose_name='Примечание',
        blank=True
    )

    def generate_path(instance, filename):
        return os.path.join('Security', str(instance.security.name)+'_'+str(instance.security.id), filename)

    photo = models.ImageField(verbose_name='Фото', upload_to=generate_path, blank=True, null=True)

    class Meta:
        verbose_name = 'Охранник'
        verbose_name_plural = 'Охранники'

    def __str__(self):
        return f'{self.security.name} {self.category} {self.status}'

class Enterprise (models.Model):
    fullname = models.CharField(
        max_length=300,
        verbose_name='Полное наименование',
        help_text='Полное наименование',
        unique=True,
    )
    abbreviatedname = models.CharField(
        max_length=300,
        verbose_name='Сокращенное наименование',
        help_text='Сокращенное наименование',
        unique=True,
    )
    legaladdress = models.CharField(
        max_length=300,
        verbose_name='Юридический адрес',
        help_text='Юридический адрес',
        blank=True
    )
    postaladdress = models.CharField(
        max_length=300,
        verbose_name='Почтовый адрес',
        help_text='Почтовый адрес',
        blank=True
    )
    telephone = models.CharField(
        max_length=30,
        verbose_name='Телефон/факс',
        help_text='Телефон/факс',
        blank=True
    )
    inn = models.CharField(
        max_length=10,
        verbose_name='ИНН',
        help_text='ИНН',
        blank=True
    )
    kpp = models.CharField(
        max_length=10,
        verbose_name='КПП',
        help_text='КПП',
        blank=True
    )
    ogrn = models.CharField(
        max_length=13,
        verbose_name='ОГРН',
        help_text='ОГРН',
        blank=True
    )
    payment = models.CharField(
        max_length=22,
        verbose_name='Рассчётный счёт',
        help_text='Рассчётный счёт',
        blank=True
    )
    correspondent = models.CharField(
        max_length=22,
        verbose_name='Корреспондентский счёт',
        help_text='Корреспондентский счёт',
        blank=True
    )
    bic = models.CharField(
        max_length=9,
        verbose_name='БИК банка',
        help_text='БИК банка',
        blank=True
    )
    bank = models.CharField(
        max_length=300,
        verbose_name='Банк',
        help_text='Банк',
        blank=True
    )
    bigboss = models.ForeignKey(
        Worker,
        verbose_name='Ген. директор',
        help_text='Ген. директор',
        null=True,
        on_delete=models.SET_NULL,
        related_name='bigboss',
        blank=True
    )

    class Meta:
        verbose_name = 'Предприятие'
        verbose_name_plural = 'Предприятия'

    def __str__(self):
        return self.abbreviatedname

class WeaponsPermit(models.Model):
    series = models.CharField(
        max_length=4,
        verbose_name='Серия',
        choices=PERMIT_SERIES,
        default='РСЛа'
    )
    number = models.CharField(
        verbose_name='Номер',
        max_length=7,
    )
    security = models.ForeignKey(
        Security,
        verbose_name='Охранник',
        on_delete=models.CASCADE,
        related_name='permits',
    )
    enterprise = models.ForeignKey(
        Enterprise,
        verbose_name='Предприятие',
        on_delete=models.CASCADE
    )
    weapon = models.ForeignKey(
        Weapon,
        verbose_name='Оружие',
        on_delete=models.CASCADE,
        related_name='weapons',
    )
    issue = models.DateField(
        verbose_name='Дата выдачи',
    )

    class Meta:
        verbose_name = 'Разрешение на хранение и ношение оружия'
        verbose_name_plural = 'Разрешения на хранение и ношение оружия'

    def __str__(self):
        return f'{self.series}№{self.number} {self.security.security.name} {self.enterprise.abbreviatedname}'

    def clean(self):
        if not re.fullmatch(r'^\d{7}', str(self.number)):
            raise ValidationError(
                {'number': 'Семь цифр номера'}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

class PersonalCard(models.Model):
    series = models.CharField(
        max_length=2,
        verbose_name='Серия',
        default='78'
    )
    number = models.CharField(
        verbose_name='Номер',
        max_length=13,
    )
    security = models.ForeignKey(
        Security,
        verbose_name='Охранник',
        on_delete=models.CASCADE,
        related_name='cards',
    )
    enterprise = models.ForeignKey(
        Enterprise,
        verbose_name='Предприятие',
        on_delete=models.CASCADE
    )
    type = models.CharField(
        max_length=12,
        verbose_name='Тип',
        choices=TYPES,
        default='основное'
    )
    issue = models.DateField(
        verbose_name='Дата выдачи',
    )

    class Meta:
        verbose_name = 'Личная карточка охранника'
        verbose_name_plural = 'Личные карточки охранников'

    def __str__(self):
        return f'{self.series}№{self.number} {self.security.security.name} {self.enterprise.abbreviatedname}-{self.type}'

    def clean(self):
        if not re.fullmatch(r'^\d{2}', str(self.series)):
            raise ValidationError(
                {'series': 'Две цифры'}
            )
        if not re.fullmatch(r'^\d{6}[А-Я]\d{6}', str(self.number)):
            raise ValidationError(
                {'number': 'Шесть цифр буква шесть цифр'}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Responseteam(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='Название ГБР',
        help_text='Название ГБР',
    )
    phone = models.CharField(
        max_length=50,
        verbose_name='Телефон ГБР',
        help_text='Телефон ГБР',
    )

    class Meta:
        verbose_name = 'Группа реагирования'
        verbose_name_plural = 'Группы реагирования'

    def __str__(self):
        return self.name

