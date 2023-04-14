import datetime as dt
import re
from dataclasses import fields

import django_filters
from dal import autocomplete
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages import constants as messages
from django.forms.models import inlineformset_factory

from Project_A.settings import (MAIN, PERMIT_SERIES, SECURITY_CATEGORY,
                                SECURITY_STATUS, SERIES, WEAPONMIN)

from .models import (Enterprise, PersonalCard, Position, Security, Weapon,
                     WeaponsPermit, Worker)


class WorkersFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='contains')
    post = django_filters.ModelChoiceFilter(queryset=Position.objects.all())
    class Meta:
        model = Worker
        fields = ('name','post')

class BaseConfirmModelForm(forms.ModelForm):
    force = forms.BooleanField(required=True, label='создать новый:')
    name = forms.Textarea()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'readonly': True})

class WorkerForm(forms.ModelForm):
    def clean_name(self):
        data = self.cleaned_data['name']
        if not re.fullmatch(r'^[А-ЯЁ][а-яё]+[\S]+[\s][А-ЯЁ][а-яё]+[\s][А-ЯЁ][\D]+', str(data)):
            raise forms.ValidationError('Фамилия Имя Отчество')
        return data
    
    class Meta:
        model = Worker
        fields = ('name','post',)
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Фамилия Имя Отчество', 'style':'width:300px'}),
            }
        
class ConfirmWorkerForm(WorkerForm, BaseConfirmModelForm):
    pass

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
        fields = (
            #'security', 
            'photo', 'epp', 'medical', 'category',
            'id_number', 'status', 'issue', 'prolonged', 'note'
        )
        widgets = {
            #'security': autocomplete.ModelSelect2(url='worker-autocomplete', attrs={'style':'width:400px'}),
            'epp': forms.TextInput(attrs={'class': 'vDateField', 'type': 'date'}),
            'medical': forms.TextInput(attrs={'class': 'vDateField', 'type': 'date'}),
            'id_number': forms.TextInput(attrs={'placeholder': 'А 123456', 'style':'width:70px'}),
            'issue': forms.TextInput(attrs={'class': 'vDateField', 'type': 'date'}),
            'prolonged': forms.TextInput(attrs={'class': 'vDateField', 'type': 'date'}),
            'note': forms.Textarea(attrs={'rows': 2,'cols': 65})
            }
        
class SecurityCreateForm(SecurityForm):
    security = forms.ModelChoiceField(
        label = 'Охранник',
        queryset=Worker.objects.all(),
        widget=autocomplete.ModelSelect2(url='worker-autocomplete', attrs={'style':'width:400px'})
        )

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
        
SecurityFormset = inlineformset_factory(Worker, Security, form=SecurityForm)

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