from django import forms
from django.contrib.admin.widgets import (AdminDateWidget,
                                          FilteredSelectMultiple)
from django.contrib.auth import get_user_model
from django.forms.models import inlineformset_factory
from pyexpat import model

from .models import (Application, Individual, Legal, Phone, Phonebook,
                     Responsible)


class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phonebook
        exclude = ()
        fields = ('phone',)

class ContactForm(forms.ModelForm):
    class Meta:
        model = Responsible
        exclude = ()
        fields = ('last_name', 'first_name', 'fathers_name', 'phone',)

class ResponsibleForm(forms.ModelForm):
    class Meta:
        model = Responsible
        fields = ('last_name', 'first_name', 'fathers_name', 'phone',)
        widgets = {
            'phone':FilteredSelectMultiple(u'телефоны', False),
        }

    class Media:
        css = {
            'all': ['admin/css/widgets.css'],
        }
        js = ['/admin/jsi18n/']

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

PhoneFormset = inlineformset_factory(Responsible, Phonebook, form=PhoneForm, extra=1)
