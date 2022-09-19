from django.contrib.auth import get_user_model
from django.db import models

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
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
    
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
        #default=datetime.date.today()
    )

    class Meta:
        verbose_name = 'Физическое лицо'
        verbose_name_plural = 'Физические лица'

    def __str__(self):
        return f'{self.name}'

class Application(models.Model):
    ANDROMEDA = 'andromeda'
    RITM = 'ritm'
    NAVIGARD = 'navigard'
    ELDES = 'eldes'
    JABLOTRON = 'jablotron'
    DX = 'dx'
    OTHER ='other'

    NEW = 'новый'
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
        (CHANGED, 'Изменён'),
        (COMPLETED, 'Завершен'),
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Новый',
        verbose_name='Статус заявки',
    )
    legal = models.ForeignKey(
        Legal,
        verbose_name='Юр.лицо',
        help_text='Юр.лицо',
        on_delete=models.CASCADE,
        related_name='legal_app',
        blank=True,
    )
    individual = models.ForeignKey(
        Individual,
        verbose_name='Физ.лицо',
        help_text='Физ.лицо',
        on_delete=models.CASCADE,
        related_name='individ_app',
        blank=True,
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
        verbose_name = 'Заявка на охрану'
        verbose_name_plural = 'Заявки на охрану'

    def __str__(self):
        return f'{self.account} {self.legal}{self.individual} {self.object_name} {self.address[:20]}...'
