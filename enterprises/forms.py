import datetime as dt
import re
from dataclasses import fields

import django_filters
from dal import autocomplete
from django import forms

from Project_A.settings import (MAIN, SECURITY_CATEGORY, SECURITY_STATUS,
                                WEAPONMIN, PERMIT_SERIES, SERIES)

from .models import (Enterprise, PersonalCard, Position, Security, Weapon,
                     WeaponsPermit, Worker)


class SecurityFilter(django_filters.FilterSet):
    security = django_filters.CharFilter(field_name='security__name', lookup_expr='contains')
    category = django_filters.ChoiceFilter(choices=SECURITY_CATEGORY)
    id_number = django_filters.CharFilter(field_name='id_number', lookup_expr='contains')
    status = django_filters.ChoiceFilter(choices=SECURITY_STATUS)
    
    class Meta:
        model = Security
        fields = [
            'security', 'epp', 'medical', 'category', 'id_number',
            'status', 'issue', 'prolonged', 'note'
        ]

class PersonalCardsFilter(django_filters.FilterSet):
    series = django_filters.CharFilter(field_name='series', lookup_expr='contains')
    number = django_filters.CharFilter(field_name='number', lookup_expr='contains')
    security = django_filters.CharFilter(field_name='security__security__name', lookup_expr='contains')
    enterprise = django_filters.ModelChoiceFilter(queryset=Enterprise.objects.all())
    class Meta:
        model = PersonalCard
        fields = ('series', 'number', 'security', 'enterprise', 'type', 'issue')

class WeaponsPermitsFilter(django_filters.FilterSet):
    series = django_filters.ChoiceFilter(choices=PERMIT_SERIES)
    number = django_filters.CharFilter(field_name='number', lookup_expr='contains')
    security = django_filters.CharFilter(field_name='security__name', lookup_expr='contains')
    enterprise = django_filters.ModelChoiceFilter(queryset=Enterprise.objects.all())
    weapon_series = django_filters.ChoiceFilter(field_name='weapon__series', choices=SERIES)
    weapon_number = django_filters.CharFilter(field_name='weapon__number', lookup_expr='contains')
    class Meta:
        model = WeaponsPermit
        fields = ('series', 'number', 'security', 'enterprise', 'weapon', 'issue')

class SecurityForm(forms.ModelForm):
    class Meta:
        model = Security
        exclude = ()
        fields = (
            'security', 'photo', 'epp', 'medical', 'category',
            'id_number', 'status', 'issue', 'prolonged', 'note'
        )
        widgets = {
            'security': autocomplete.ModelSelect2(url='worker-autocomplete', attrs={'style':'width:400px'}),
            'epp': forms.TextInput(attrs={'class': 'vDateField', 'type': 'date'}),
            'medical': forms.TextInput(attrs={'class': 'vDateField', 'type': 'date'}),
            'id_number': forms.TextInput(attrs={'placeholder': 'А 123456', 'style':'width:70px'}),
            'issue': forms.TextInput(attrs={'class': 'vDateField', 'type': 'date'}),
            'prolonged': forms.TextInput(attrs={'class': 'vDateField', 'type': 'date'}),
            'note': forms.Textarea(attrs={'rows': 2,'cols': 65})
            }

class PersonalCardForm(forms.ModelForm):
    class Meta:
        model = PersonalCard
        exclude = ()
        fields = ('series', 'number', 'security', 'enterprise', 'type', 'issue')
        widgets = {
            'series': forms.TextInput(attrs={'placeholder': '78', 'style':'width:50px'}),
            'number': forms.TextInput(attrs={'placeholder': '123456Б123456 ', 'style':'width:100px'}),
            'issue': forms.TextInput(attrs={'class': 'vDateField', 'type': 'date'}),
            }

class WeaponForm(forms.ModelForm):
    class Meta:
        model = Weapon
        exclude = ()
        fields = ('model', 'caliber', 'series', 'number', 'release')
        widgets = {
            'number': forms.TextInput(attrs={'placeholder': '1234', 'style':'width:70px'}),
            'release': forms.NumberInput(attrs={'style':'width:70px'})
            }

class WeaponsPermitForm(forms.ModelForm):
    class Meta:
        model = WeaponsPermit
        exclude = ()
        fields = ('series', 'number', 'security', 'enterprise', 'weapon', 'issue')
        widgets = {
            'number': forms.TextInput(attrs={'placeholder': '1234567', 'style':'width:100px'}),
            'issue': forms.TextInput(attrs={'class': 'vDateField', 'type': 'date'}),
            }

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