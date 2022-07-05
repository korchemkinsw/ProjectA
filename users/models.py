from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .manager import CustomUserManager


class CustomUser(AbstractUser):
    ADMIN = 'admin'
    USER = 'user'
    DIRECTOR = 'director'
    ENGINEER = 'engineer'
    TECHNICAN ='technican'
    SECRETARY = 'secretary'
    ROLE_CHOICES = (
        (ADMIN, 'Администратор'),
        (USER, 'Пользователь'),
        (DIRECTOR, 'Директор'),
        (ENGINEER, 'Инженер ПЦО'),
        (TECHNICAN, 'Техник'),
        (SECRETARY, 'Секретарь'),
    )
    email = models.EmailField(_('email address'), unique=True)
    
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
    username = models.CharField(
        max_length=150,
        blank=True,
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name='уровень доступа',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.last_name} {self.first_name[:1]}.{self.fathers_name[:1]}. {self.email}'
