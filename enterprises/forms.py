from dataclasses import fields

from django import forms

from .models import Enterprise, Position, Worker


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
        model = Worker
        fields = (
            'name',
            'post',
        )