import django_filters
from django import forms
from django.contrib.admin.widgets import (AdminDateWidget,
                                          FilteredSelectMultiple)
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from orders.forms import DateInput

from .models import Contact, Individual, Legal, Responsible


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

class ResponsibleFilter(django_filters.FilterSet):
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='contains')
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='contains')
    fathers_name = django_filters.CharFilter(field_name='fathers_name', lookup_expr='contains')
    #phone = django_filters.CharFilter(field_name='phone', lookup_expr='contains')

    class Meta:
        model = Responsible
        fields = ['last_name', 'first_name', 'fathers_name']

class IndividualForm(forms.ModelForm):
    class Meta:
        model = Individual
        exclude = ()
        fields = ['num_pass', 'issued', 'date']
        widgets = {'date': DateInput()}

    def __init__(self, *args, **kwargs):
        super(IndividualForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget=AdminDateWidget()

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

class BaseContactFormset(BaseInlineFormSet):
    pass

ContactFormset = inlineformset_factory(Responsible, Contact, form=ContactsForm,extra=1)
