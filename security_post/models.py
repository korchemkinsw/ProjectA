from django.db import models

from clientele.models import Contact, Contract, Individual, Legal
from enterprises.models import Enterprise, Responseteam, Security
from Project_A.settings import SHIFTS


class GuardObject(models.Model):
    contract = models.ForeignKey(
        Contract,
        verbose_name='Договор',
        help_text='Договор',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='contract_post',
    )
    qteam = models.ForeignKey(
        Responseteam,
        verbose_name='Группа реагирования',
        on_delete=models.CASCADE,
        related_name='team_post',
        null=True,
        blank=True,
    )
    number = models.PositiveIntegerField(
        verbose_name='количество постов',
        help_text='количество постов',
    )

    class Meta:
        verbose_name = 'Объект охраны'
        verbose_name_plural = 'Объекты охраны'

    def __str__(self):
        if self.contract.legal:
            return f'{self.contract.legal}, постов: {self.number}: {self.contract.enterprise}'
        if self.contract.individual:
            return f'{self.contract.individual}, постов: {self.number}: {self.contract.enterprise}'
        if self.qteam:
            return f'{self.qteam.name}: {self.qteam.enterprise}'

class GuardPost(models.Model):
    guard_object = models.ForeignKey(
        GuardObject,
        verbose_name='Объект охраны',
        help_text='Объект охраны',
        on_delete=models.CASCADE,
        related_name='guard_objects',
    )
    number = models.PositiveIntegerField(
        verbose_name='количество сотрудников',
        help_text='количество сотрудников',
    )
    personnel = models.ManyToManyField(
        Security,
        through='GuardsOnDuty',
        related_name='post_personnel',
        verbose_name='Сотрудники',
    )
    
    note = models.CharField(
        max_length=200,
        verbose_name='Примечание',
        blank=True
    )

    class Meta:
        verbose_name = 'Пост охраны'
        verbose_name_plural = 'Посты охраны'

    def __str__(self):
        return f'Пост из {self.number} сотрудников на {self.guard_object}'

class WorkingShift(models.Model):
    security = models.ForeignKey(
        Security,
        verbose_name='Охранник',
        help_text='Охранник',
        on_delete=models.CASCADE,
        related_name='shift_posts',
    )
    shift = models.CharField(
        max_length=5,
        choices=SHIFTS,
        verbose_name='Смена',
    )
    begin = models.DateField(
        verbose_name='Начало смены',
    )
    end = models.DateField(
        verbose_name='Конец смены',
    )

    class Meta:
        verbose_name = 'Дежурная смена'
        verbose_name_plural = 'Дежурные смены'

    def __str__(self):
        return f'Пост {self.security} {self.shift}'

class GuardsOnDuty(models.Model):
    security = models.ForeignKey(
        Security,
        on_delete=models.CASCADE,
        verbose_name='Сотрудник',
        related_name='security_in_post'
    )
    post = models.ForeignKey(
        GuardPost,
        on_delete=models.CASCADE,
        verbose_name='Смена',
        related_name='posts_security'
    )

    class Meta:
        verbose_name = 'Сотрудники поста охраны'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'Пост {self.security} на {self.shift}'