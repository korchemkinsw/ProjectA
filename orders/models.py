from pyexpat import model
from telnetlib import NEW_ENVIRON
from tkinter import CASCADE
from django.db import models

from users.models import CustomUser
from enterprises.models import Enterprise


class FileOrder(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(verbose_name='Файл приказа')  
    
    class Meta:
        verbose_name='Файл приказа'
        verbose_name_plural = 'Файл приказа'

    #def __str__(self):
    #    return self.file

class Order(models.Model):
    NEW = 'новый'
    INWORK = 'в работе'
    PENDING = 'ожидающий'
    COMPLETED = 'завершен'
    REDJECTED = 'отклонен'
    EXPIRED = 'Просрочен!'

    ACCEPT = 'Принять'
    REOPEN = 'Возобновить'
    REMOVE = 'Снять'
    SUSPEND = 'Приостановить'

    STATUS_CHOICES = (
        (NEW, 'Новый'),
        (INWORK, 'В работе'),
        (PENDING, 'Ожидающий'),
        (COMPLETED, 'Завершен'),
        (REDJECTED, 'Отклонен'),
        (EXPIRED, 'Просрочен!')
    )

    ACTION_CHOICES = (
        (ACCEPT, 'Принять'),
        (REOPEN, 'Возобновить'),
        (REMOVE, 'Снять'),
        (SUSPEND, 'Приостановить'),
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=NEW,
        verbose_name='Статус приказа',
    )
    lastuser = models.ForeignKey(
        CustomUser,
        verbose_name="Последний пользователь",
        help_text="Последний пользователь",
        null=True,
        on_delete=models.SET_NULL,
        related_name="lastuser",
    )
    firm = models.ForeignKey(
        Enterprise,
        verbose_name="Предприятие",
        help_text="Предприятие",
        on_delete=models.CASCADE,
        related_name="firm",
    )
    action = models.CharField(
        max_length=15,
        choices=ACTION_CHOICES,
        default=NEW,
        verbose_name='Что сделать?',
    )
    generated = models.DateTimeField(
        "Дата создания",
        auto_now_add=True
    )
    perday = models.DateTimeField(
        "Выполнить в",
        auto_now_add=True
    )
    contractor = models.ManyToManyField(
        CustomUser,
        through='ContractorsOrder',
        related_name='contractors_order',
    )
    order = models.ManyToManyField(
        FileOrder,
        through='FilesOrder',
        related_name='files_order',
        verbose_name='Файлы приказа'
    )

    class Meta:
        verbose_name = "Приказ"
        verbose_name_plural = 'Приказы'

    def __str__(self):
        return f'{self.status} {self.action} {self.firm}'

class ContractorsOrder(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name='Приказ',
        null=True,
        on_delete=models.SET_NULL,
    )
    contractor = models.ForeignKey(
        CustomUser,
        verbose_name='Исполнители',
        on_delete=models.CASCADE
    )

class FilesOrder(models.Model):
    order=models.ForeignKey(
        Order,
        verbose_name='Приказ',
        null=True,
        on_delete=models.SET_NULL,
    )
    file = models.ForeignKey(
        FileOrder,
        on_delete=CASCADE,
        verbose_name='Файлы приказа'
    )

