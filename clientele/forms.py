import django_filters
from core.widgets import FengyuanChenDatePickerInput
from django import forms
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from object_card.models import Card
from pyexpat import model

from .models import (Contact, Contract, FileContract, Individual, Legal,
                     Responsible)


class ContactsForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ()
        fields = ('type', 'phone',)

class ContactForm(forms.ModelForm):
    class Meta:
        model = Responsible
        exclude = ()
        fields = ('last_name', 'first_name', 'fathers_name',)
        labels ={
            'last_name': 'Фамилия',
            'first_name': 'Имя',
            'fathers_name': 'Отчество',
        }

class DateInput(forms.DateInput):
    input_type = 'date'

class ContactFilter(django_filters.FilterSet):
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='contains')
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='contains')
    fathers_name = django_filters.CharFilter(field_name='fathers_name', lookup_expr='contains')
    phone = django_filters.CharFilter(field_name='contacts__phone', lookup_expr='exact')

    class Meta:
        model = Contact
        fields = ['last_name', 'first_name', 'fathers_name', 'phone',]

class IndividualForm(forms.ModelForm):
    class Meta:
        model = Individual
        exclude = ()
        fields = ['num_pass', 'issued', 'date']

    def __init__(self, *args, **kwargs):
        super(IndividualForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget=FengyuanChenDatePickerInput()

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

class ContractFilter(django_filters.FilterSet):
    enterprise = django_filters.CharFilter(field_name='enterprise__abbreviatedname', lookup_expr='contains')
    number = django_filters.CharFilter(field_name='number', lookup_expr='contains')
    legal = django_filters.CharFilter(field_name='legal__abbreviatedname', lookup_expr='contains')
    individual = django_filters.CharFilter(field_name='individual__name__last_name', lookup_expr='contains')

    class Meta:
        model = Contract
        fields = ['enterprise', 'number', 'legal', 'individual',]

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        exclude = ()
        fields = ('enterprise', 'number', 'date',)

    def __init__(self, *args, **kwargs):
            super(ContractForm, self).__init__(*args, **kwargs)
            self.fields['date'].widget=FengyuanChenDatePickerInput()

class FileContractForm(forms.ModelForm):
    class Meta:
        model = FileContract
        exclude = ()
        fields = ('contract', 'file',)

class BaseContactFormset(BaseInlineFormSet):
    pass

ContactFormset = inlineformset_factory(Responsible, Contact, form=ContactsForm,extra=1)
