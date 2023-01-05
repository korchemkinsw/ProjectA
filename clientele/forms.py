import re

import django_filters
from dal import autocomplete
from django import forms
from django.forms.models import inlineformset_factory
from enterprises.models import Enterprise

from .models import (Contact, Contract, FileContract, Individual, Legal,
                     Phone)


class PhoneForm(forms.ModelForm):
    def clean_phone(self):
        data = self.cleaned_data['phone']
        if not re.fullmatch(r'7\d{10}', str(data)):
            raise forms.ValidationError("Введен неверный номер телефона")
        return data

    class Meta:
        model = Phone
        exclude = ()
        fields = ('type', 'phone',)
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': '7XXXXXXXXXX'}),
        }

class ContactForm(forms.ModelForm):
    def clean_name(self):
        data = self.cleaned_data['name']
        if not re.fullmatch(r'^[А-ЯЁ][а-яё]+[\S]+[\s][А-ЯЁ][а-яё]+[\s][А-ЯЁ][\D]+', str(data)):
            raise forms.ValidationError("Фамилия Имя Отчество")
        return data

    class Meta:
        model = Contact
        exclude = ()
        fields = ('name',)
        labels ={
            'name': 'Фамилия Имя Отчество',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Фамилия Имя Отчество'}),
        }

class ContactFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='contains')
    phone = django_filters.CharFilter(field_name='contacts__phone', lookup_expr='exact')

    class Meta:
        model = Contact
        fields = ['name', 'phone',]

class IndividualForm(forms.ModelForm):
    def clean_num_pass(self):
        data = self.cleaned_data['num_pass']
        if not re.fullmatch(r'^[0-9]{4}[\s][0-9]{6}', data):
            raise forms.ValidationError("Серия и номер паспорта в формате: ХХХХ ХХХХХХ")
        return data

    class Meta:
        model = Individual
        exclude = ()
        fields = ['num_pass', 'issued', 'date']
        widgets = {
            'num_pass': forms.TextInput(attrs={'placeholder': 'XXXX XXXXXX'}),
            'date': forms.TextInput(attrs={'class': 'vDateField', 'type': 'date'}),
        }

class LegalForm(forms.ModelForm):
    class Meta:
        model = Legal
        exclude = ()
        fields = [
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
        ]

class IndividualFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name__name', lookup_expr='contains')
    
    class Meta:
        model = Individual
        fields = ['name',]

class LegalFilter(django_filters.FilterSet):
    fullname = django_filters.CharFilter(field_name='fullname', lookup_expr='contains')
    inn = django_filters.CharFilter(field_name='inn', lookup_expr='contains')

    class Meta:
        model = Legal
        fields = ['fullname', 'inn']

class ContractFilter(django_filters.FilterSet):
    enterprise = django_filters.ModelChoiceFilter(queryset=Enterprise.objects.all())
    number = django_filters.CharFilter(field_name='number', lookup_expr='contains')
    legal = django_filters.CharFilter(field_name='legal__fullname', lookup_expr='contains')
    individual = django_filters.CharFilter(field_name='individual__name__name', lookup_expr='contains')

    class Meta:
        model = Contract
        fields = ['enterprise', 'number', 'legal', 'individual',]

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        exclude = ()
        fields = ('enterprise', 'number', 'date',)
        widgets = {
            'enterprise': autocomplete.ModelSelect2(url='enterprise-autocomplete', attrs={'style':'width:400px'}),
            'date': forms.TextInput(attrs={'class': 'vDateField', 'type': 'date'}),
            }

class FileContractForm(forms.ModelForm):
    file = forms.FileField(label='Добавить/изменить', widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = FileContract
        exclude = ()
        fields = ('title', 'file',)

PhoneFormset = inlineformset_factory(Contact, Phone, form=PhoneForm, extra=1)
ContractFormset = inlineformset_factory(Contract, FileContract, form=FileContractForm, extra=1)
