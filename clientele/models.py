import datetime
import os
from email.policy import default
from trace import Trace

from django.contrib.auth import get_user_model
from django.db import models
from enterprises.models import Enterprise

User = get_user_model()


class Responsible(models.Model):
    last_name = models.CharField(
        verbose_name='фамилия',
        max_length=150,
    )
    first_name = models.CharField(
        verbose_name='имя',
        max_length=150,
    )
    fathers_name = models.CharField(
        verbose_name='отчество',
        max_length=150,
        blank=True
    )

    class Meta:
        verbose_name = 'Ответственное лицо'
        verbose_name_plural = 'Ответственные лица'

    def __str__(self):
        return f'{self.last_name} {self.first_name[:1]}.{self.fathers_name[:1]}.'

class Contact(models.Model):
    MOBILE = 'мобильный'
    HOME = 'домашний'
    WORKER = 'рабочий'

    TYPES = (
        (MOBILE, 'мобильный'),
        (HOME, 'домашний'),
        (WORKER, 'рабочий')
    )
    responsible = models.ForeignKey(
        Responsible,
        verbose_name='Ответственное лицо',
        on_delete=models.CASCADE,
        related_name='contacts',
        blank=True,
    )
    type = models.CharField(
        max_length=10,
        choices=TYPES,
        verbose_name='тип телефона',
    )
    phone = models.CharField(
        verbose_name='номер телефона',
        max_length=11,
        unique=True
    )

    class Meta:
        verbose_name = 'Телефон'
        verbose_name_plural = 'Телефоны'
    
    def __str__(self):
        return f'{self.responsible} | {self.type} {self.phone}'

class Legal(models.Model):
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
        unique=True
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
        Responsible,
        verbose_name='Ген. директор',
        help_text='Ген. директор',
        null=True,
        on_delete=models.SET_NULL,
        related_name='bigboss',
        blank=True
    )

    class Meta:
        verbose_name = 'Юридическое лицо'
        verbose_name_plural = 'Юридические лица'

    def __str__(self):
        return self.abbreviatedname

class Individual(models.Model):
    name = models.ForeignKey(
        Responsible,
        verbose_name='Клиент',
        help_text='Клиент',
        on_delete=models.CASCADE,
        related_name='individual',
    )
    num_pass = models.CharField(
        max_length=11,
        verbose_name='Серия и номер паспорта',
        help_text='Серия и номер паспорта',
        unique=True
    )
    issued = models.CharField(
        max_length=150,
        verbose_name='Кем выдан',
        help_text='Кем выдан',
        blank=True,
    )
    date = models.DateField(
        verbose_name='Дата выдачи',
        help_text='Дата выдачи',
        blank=True,
    )

    class Meta:
        verbose_name = 'Физическое лицо'
        verbose_name_plural = 'Физические лица'

    def __str__(self):
        return f'{self.name}'

class Contract(models.Model):
    NEW = 'новый'
    CURRENT = 'действующий'
    SUSPENDED = 'приостановлен'
    CLOSED = 'закрыт'

    STATUS_CHOICES = (
        (NEW, 'новый'),
        (CURRENT, 'действующий'),
        (SUSPENDED, 'приостановлен'),
        (CLOSED, 'закрыт'),
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='новый',
        verbose_name='Статус договора',
    )
    number = models.CharField(
        max_length=10,
        verbose_name='Номер договора',
        help_text='Номер договора',
        unique=True
    )
    date = models.DateField(
        verbose_name='Дата договора',
        help_text='Дата договора',
        blank=True,
    )
    enterprise = models.ForeignKey(
        Enterprise,
        verbose_name='Предприятие',
        help_text='Предприятие',
        null=True,
        on_delete=models.SET_NULL,
        related_name='enterprise',
    )
    legal = models.ForeignKey(
        Legal,
        verbose_name='Клиент ЮЛ',
        help_text='Клиент ЮЛ',
        null=True,
        on_delete=models.SET_NULL,
        related_name='legal',
        blank=True,
    )
    individual = models.ForeignKey(
        Individual,
        verbose_name='Клиент ФЛ',
        help_text='Клиент ФЛ',
        null=True,
        on_delete=models.SET_NULL,
        related_name='individual',
        blank=True,
    )
    contractholder=models.ForeignKey(
        User,
        verbose_name='От предприятия:',
        on_delete=models.SET_NULL,
        related_name='contractholder',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Договора'

    def __str__(self):
        return f'{self.number} от {self.date}'

class FileContract(models.Model):
    contract = models.ForeignKey(
        Contract,
        verbose_name='договор',
        null=True,
        on_delete=models.CASCADE,
        related_name='files'
    )
    title = models.CharField(
        max_length=30,
        verbose_name='Документ:',
        help_text='Документ:',
    )
    generated = models.DateTimeField(
        'Дата создания',
        null=True,
        blank=True,
        default=datetime.datetime.today()
    )

    def generate_path(instance, filename):
        enterprise=str(instance.contract.enterprise)
        contract=str(instance.contract.number)+'-'+str(instance.contract.date)
        for simb, new in (" ", "-"), ("/", "-"), ('"', ""):
            enterprise=enterprise.replace(simb, new)
            contract=contract.replace(simb, new)
        return os.path.join('clientele/contracts', enterprise+"/"+contract, filename)

    file = models.FileField(verbose_name='Файл договора', upload_to=generate_path)

    def delete(self, *args, **kwargs):
        storage, path = self.file.storage, self.file.path
        super(FileContract,self).delete(*args,**kwargs)
        storage.delete(path)
    
    class Meta:
        verbose_name='Файл договора'
        verbose_name_plural = 'Файлы договоров'

    def __str__(self):
        return (
            f'Договор №{self.contract}; '
            f'Файл: {self.file} '
        )
