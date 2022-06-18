import datetime

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import models
from enterprises.models import Enterprise
from users.models import CustomUser

User = get_user_model()

class FileOrder(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(verbose_name='Файл приказа', upload_to='orders/%Y-%m-%d/')
    
    class Meta:
        verbose_name='Файл приказа'
        verbose_name_plural = 'Файл приказа'

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
        #(NEW, 'Новый'),
        (INWORK, 'В работе'),
        (PENDING, 'Ожидающий'),
        (COMPLETED, 'Завершен'),
        (REDJECTED, 'Отклонен'),
        #(EXPIRED, 'Просрочен!')
    )

    ACTION_CHOICES = (
        (ACCEPT, 'Принять'),
        (REOPEN, 'Возобновить'),
        (REMOVE, 'Снять'),
        (SUSPEND, 'Приостановить'),
    )

    author = models.ForeignKey(
        CustomUser,
        verbose_name="Автор",
        null=True,
        on_delete=models.SET_NULL,
        related_name="author",
    )
    number = models.CharField(
        max_length=10,
        verbose_name='Номер приказа',
        null=True,
    )
    generated = models.DateTimeField(
        "Дата создания",
        auto_now_add=True
    )
    firm = models.ForeignKey(
        Enterprise,
        verbose_name="Предприятие",
        null=True,
        on_delete=models.CASCADE,
        related_name="firm",
    )
    action = models.CharField(
        max_length=15,
        choices=ACTION_CHOICES,
        verbose_name='Что сделать?',
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Новый',
        verbose_name='Статус приказа',
    )
    perday = models.DateField(
        "Выполнить в",
        default=datetime.date.today()
    )
    comment = models.CharField(
        max_length=300,
        verbose_name='Комментарий',
        blank=True
    )
    changed = models.DateTimeField(
        "Дата изменения",
        auto_now_add=True,
    )
    lastuser = models.ForeignKey(
        CustomUser,
        verbose_name="Последний пользователь",
        null=True,
        on_delete=models.SET_NULL,
        related_name="lastuser",
        blank=True
    )
    contractor = models.ManyToManyField(
        User,
        through='ContractorsOrder',
        related_name='contractors_order',
        blank=True,
    )
    order = models.ManyToManyField(
        FileOrder,
        through='FilesOrder',
        related_name='files_order',
        verbose_name='Файлы приказа',
        blank=True,
    )

    class Meta:
        verbose_name = "Приказ"
        verbose_name_plural = 'Приказы'

   # def get_absolute_url(self):
   #     return reverse('update_order', kwargs={'pk': self.pk})

    def __str__(self):

        return f'{self.generated.date()} {self.action} {self.firm}'

class ContractorsOrder(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name='Приказ',
        null=True,
        on_delete=models.SET_NULL,
        related_name="contractors",
    )
    contractor = models.ForeignKey(
        CustomUser,
        verbose_name='Исполнитель',
        on_delete=models.CASCADE,
        related_name="contractors",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'

class FilesOrder(models.Model):
    order=models.ForeignKey(
        Order,
        verbose_name='Приказ',
        null=True,
        on_delete=models.SET_NULL,
        related_name="files",
    )
    file = models.ForeignKey(
        FileOrder,
        on_delete=models.CASCADE,
        verbose_name='Файлы приказа',
        related_name="files",
        blank=True,
        null=True
    )

    #file = models.FileField(verbose_name='Файл приказа', upload_to='orders/%Y-%m-%d/')

    class Meta:
        verbose_name = 'Файл приказа'
        verbose_name_plural = 'Файлы приказа'