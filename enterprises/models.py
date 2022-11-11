from django.db import models
from django.utils.text import slugify


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

class Staffer(models.Model):
    last_name = models.CharField(
        verbose_name='фамилия',
        max_length=150,
        blank=True
    )
    first_name = models.CharField(
        verbose_name='имя',
        max_length=150,
        blank=True
    )
    fathers_name = models.CharField(
        verbose_name='отчество',
        max_length=150,
        blank=True
    )
    post = models.ForeignKey(
        Position,
        verbose_name="Должность",
        help_text="Должность",
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
    
    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.fathers_name}'

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
        Staffer,
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

