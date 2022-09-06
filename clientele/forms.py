from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth import get_user_model

from .models import Application, Individual, Legal, Responsible


class LegalForm(forms.ModelForm):
    class Meta:
        model = Legal
        exclude = ()
        fields = (
            'fullname',
            'abbreviatedname',
            'legaladdress',
            'postaladdress',
            'telephone',
            'inn',
            'kpp',
            'ogrn',
            'payment',
            'correspondent',
            'bic',
            'bank',
            'bigboss',
        )

