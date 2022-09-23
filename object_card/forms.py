from dataclasses import fields
from email.mime import application

import django_filters
from betterforms.multiform import MultiModelForm
from clientele.models import Application
from django import forms
from django.forms.models import BaseInlineFormSet, inlineformset_factory

from .models import Card, Contract, Device, Partition, Zone


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        exclude = ()
        fields = ('account', 'device', 'sim_first', 'sim_two',)

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        exclude =()
        fields = ('number', 'enterprise', 'qteam',)

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        exclude =()
        fields = ('device', 'application', 'contract',)

class CardDeviceForm(forms.ModelForm):
    class Meta:
        model = Card
        exclude =()
        fields = ('application',)
    '''
    class Meta:
        model = Card
        exclude = ()
        fields = ('application',)
    
    def __init__(self, *args, **kwargs):
        super (CardDeviceForm,self ).__init__(*args,**kwargs)
        self.fields['application'].queryset = Application.objects.filter(status=Application.NEW)
    '''
CardDeviceFormset=inlineformset_factory(Device, Card, form=CardDeviceForm, extra=1)
