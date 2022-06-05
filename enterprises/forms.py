from dataclasses import fields
from django import forms
from .models import Enterprise, Position, Staffer

class AddEnterpriseForm(forms.ModelForm):
    class Meta:
        model = Enterprise
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


class AddPositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ('post',)

class AddStafferForm(forms.ModelForm):
    class Meta:
        model = Staffer
        fields = (
            'last_name',
            'first_name',
            'fathers_name',
            'post',
        )