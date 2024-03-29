import os

from django.contrib.auth import get_user_model
from django.db import models

from enterprises.models import Enterprise
from users.models import CustomUser

User = get_user_model()

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
        #(PENDING, 'Ожидающий'),
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

    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор',
        null=True,
        on_delete=models.SET_NULL,
        related_name='author',
    )
    number = models.CharField(
        max_length=10,
        verbose_name='Номер приказа',
        null=True,
    )
    generated = models.DateTimeField(
        'Дата создания',
        null=True,
        blank=True,
        #auto_now_add=True
    )
    firm = models.ForeignKey(
        Enterprise,
        verbose_name='Предприятие',
        null=True,
        on_delete=models.CASCADE,
        related_name='firm',
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
        'Выполнить в',
        #default=datetime.date.today()
    )
    comment = models.TextField(
        max_length=300,
        verbose_name='Пояснение',
        blank=True
    )
    changed = models.DateTimeField(
        'Дата изменения',
        auto_now_add=True
    )
    lastuser = models.ForeignKey(
        CustomUser,
        verbose_name='Последний пользователь',
        null=True,
        on_delete=models.SET_NULL,
        related_name='lastuser',
        blank=True
    )
    contractor = models.ManyToManyField(
        User,
        through='ContractorsOrder',
        related_name='contractors_order',
        blank=True,
    )

    class Meta:
        verbose_name = 'Приказ'
        verbose_name_plural = 'Приказы'
        ordering = ('-generated',)

    def __str__(self):
        return f'{self.number} от {self.generated} по {self.firm}'

class ContractorsOrder(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name='Приказ',
        null=True,
        on_delete=models.CASCADE,
        related_name='contractors',
    )
    contractor = models.ForeignKey(
        CustomUser,
        verbose_name='Исполнитель',
        on_delete=models.CASCADE,
        related_name='contractors',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'

    def __str__(self):
        return (
            f'Приказ №{self.order}; '
            f'Исполнитель: {self.contractor} '
        )

class FileOrder(models.Model):
    order=models.ForeignKey(
        Order,
        verbose_name='Приказ',
        null=True,
        on_delete=models.CASCADE,
        related_name='files'
    )

    def generate_path(instance, filename):
        enterprise=str(instance.order.firm.abbreviatedname)
        for simb, new in (" ", "-"), ("/", "-"), ('"', ""):
            enterprise=enterprise.replace(simb, new)
        return os.path.join('orders', str(enterprise)+"/%Y-%m-%d/", filename)

    file = models.FileField(verbose_name='Файл приказа', upload_to=generate_path)

    def delete(self, *args, **kwargs):
        storage, path = self.file.storage, self.file.path
        super(FileOrder,self).delete(*args,**kwargs)
        storage.delete(path)
    
    class Meta:
        verbose_name='Файл приказа'
        verbose_name_plural = 'Файлы приказов'

    def __str__(self):
        return (
            f'Приказ №{self.order}; '
            f'Файл: {self.file} '
        )

class CommentOrder(models.Model):
    created = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор',
        null=True,
        on_delete=models.SET_NULL,
        related_name='comments',
    )
    order=models.ForeignKey(
        Order,
        verbose_name='Приказ',
        null=True,
        on_delete=models.SET_NULL,
        related_name='comments'
    )
    comment = models.CharField(
        max_length=300,
        verbose_name='Комментарий',
        blank=True
    )

    class Meta:
        verbose_name='Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created',)

    def __str__(self):
        return (
            f'{self.author} '
            f'{self.created.date()} '
            f'{self.order} '
            f'{self.comment[:15]}...')
