import django_filters
from django import forms
from django.forms.models import inlineformset_factory

from enterprises.models import Enterprise

from .models import GuardObject, GuardPost


class GuardObjectForm(forms.ModelForm):
    class Meta:
        model = GuardObject
        exclude = ('contract', 'qteam',)

class GuardObjectFilter(django_filters.FilterSet):
    contracrt_number = django_filters.CharFilter(field_name='contract__number', lookup_expr='contains')
    contract_legal = django_filters.CharFilter(field_name='contract__legal__abbreviatedname', lookup_expr='contains')
    contract_individual = django_filters.CharFilter(field_name='contract__individual__name', lookup_expr='contains')
    
    class Meta:
        model =  GuardObject
        fields = ['contract__enterprise', 'contracrt_number', 'contract_legal', 'contract_individual']

    
        

class BaseGuardPostForm(forms.ModelForm):
    class Meta:
        model = GuardPost
        exclude = ('guard_object', 'personnel',)
        widgets = {
            'number': forms.NumberInput(attrs={'style': 'width:50px'}),
            'note': forms.Textarea(attrs={'rows': 2,'cols': 65})
            }

class GuardPostForm(forms.ModelForm):
    class Meta:
        model = GuardPost
        exclude = ('guard_object',)