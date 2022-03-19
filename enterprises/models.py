from django.db import models

from users.models import CustomUser


class Enterprise (models.Model):
    fullname = models.CharField(
        max_length=300,
        verbose_name='Полное наименование',
        help_text="Полное наименование",
        unique=True,
        default='None'
    )
    abbreviatedname = models.CharField(
        max_length=300,
        verbose_name='Сокращенное наименование',
        help_text="Сокращенное наименование",
        unique=True,
        default='None'
    )
    legaladdress = models.CharField(
        max_length=300,
        verbose_name='Юридический адрес',
        help_text="Юридический адрес",
        default='None'
    )
    postaladdress = models.CharField(
        max_length=300,
        verbose_name='Почтовый адрес',
        help_text="Почтовый адрес",
        default='None'
    )
    telephone = models.CharField(
        max_length=30,
        verbose_name='Телефон/факс',
        help_text="Телефон/факс",
        default='None'
    )
    inn = models.CharField(
        max_length=10,
        verbose_name='ИНН',
        help_text="ИНН",
        default='None'
    )
    kpp = models.CharField(
        max_length=10,
        verbose_name='КПП',
        help_text="КПП",
        default='None'
    )
    ogrn = models.CharField(
        max_length=13,
        verbose_name='ОГРН',
        help_text="ОГРН",
        default='None'
    )
    payment = models.CharField(
        max_length=22,
        verbose_name='Рассчётный счёт',
        help_text="Рассчётный счёт",
        default='None'
    )
    correspondent = models.CharField(
        max_length=22,
        verbose_name='Корреспондентский счёт',
        help_text="Корреспондентский счёт",
        default='None'
    )
    bic = models.CharField(
        max_length=9,
        verbose_name='БИК банка',
        help_text="БИК банка",
        default='None'
    )
    bank = models.CharField(
        max_length=300,
        verbose_name='Банк',
        help_text="Банк",
        default='None'
    )
    bigboss = models.ForeignKey(
        CustomUser,
        verbose_name="Ген. директор",
        help_text="Ген. директор",
        null=True,
        on_delete=models.SET_NULL,
        related_name="bigboss",
    )

    class Meta:
        verbose_name = "Предприятие"
        verbose_name_plural = 'Предприятия'

    def __str__(self):
        return self.company
