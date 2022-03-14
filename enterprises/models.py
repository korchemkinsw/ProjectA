from django.db import models

from users.models import CustomUser


class Enterprise (models.Model):
    company = models.CharField(
        max_length=30,
        verbose_name='название предприятия',
        unique=True,
    )
    bigboss = models.ForeignKey(
        CustomUser, verbose_name="Ген. директор", help_text="Ген. директор",
        null=True, on_delete=models.SET_NULL, related_name="bigboss",
    )

    class Meta:
        verbose_name = "Предприятие"
        verbose_name_plural = 'Предприятия'

    def __str__(self):
        return self.company
