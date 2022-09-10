import django_filters
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms.models import BaseInlineFormSet, inlineformset_factory

from .models import Contact, Legal, Phone, Phonebook, Responsible


class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        exclude = ()
        fields = ('type', 'phone',)

class ContactsForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ()
        fields = ('type', 'phone',)

class PhonebookForm(forms.ModelForm):
    class Meta:
        model = Phonebook
        exclude = ()
        fields = ('phone',)
  
    def __init__(self, *args, **kwargs):
        super (PhonebookForm,self ).__init__(*args,**kwargs)
        phones=Phone.objects.all()
        phonebook=Phonebook.objects.all()
        for contact in phonebook:
            phones=phones.exclude(phone=contact.phone.phone)
        self.fields['phone'].queryset = phones

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

class ResponsibleForm(forms.ModelForm):
    class Meta:
        model = Responsible
        fields = ('last_name', 'first_name', 'fathers_name', 'phone',)
        labels ={
            'last_name': 'Фамилия',
            'first_name': 'Имя',
            'fathers_name': 'Отчество',
            'phone': 'Телефон',
        }
        widgets = {
            'phone':FilteredSelectMultiple(u'телефоны', False),
        }

    class Media:
        css = {
            'all': ['admin/css/widgets.css'],
        }
        js = ['/admin/jsi18n/']

    def __init__(self, *args, **kwargs):
        super (ResponsibleForm,self ).__init__(*args,**kwargs)
        phones=Phone.objects.all()
        phonebook=Phonebook.objects.all()
        for contact in phonebook:
            phones=phones.exclude(phone=contact.phone.phone)
        self.fields['phone'].queryset = phones

class ResponsibleFilter(django_filters.FilterSet):
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='contains')
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='contains')
    fathers_name = django_filters.CharFilter(field_name='fathers_name', lookup_expr='contains')
    #phone = django_filters.CharFilter(field_name='phone', lookup_expr='contains')

    class Meta:
        model = Responsible
        fields = ['last_name', 'first_name', 'fathers_name']

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

class BaseContactFormset(BaseInlineFormSet):
    pass

ContactFormset = inlineformset_factory(Responsible, Contact, form=ContactsForm,extra=1)
