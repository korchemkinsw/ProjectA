from dataclasses import fields

import django_filters
from betterforms.multiform import MultiModelForm
from django import forms
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from enterprises.models import Responseteam

from .models import Card, Device, Partition, Sim, Zone


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        exclude = ()
        fields = ('account', 'device',)
        labels ={
            'account': 'Передаваемый номер',
            'account': 'Тип ППК',
        }

class SimForm(forms.ModelForm):
    class Meta:
        model = Sim
        exclude =()
        fields = ('iccid', 'msisdn',)

class CardFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Card.STATUS_CHOICES)
    account = django_filters.CharFilter(field_name='device__account', lookup_expr='contains')
    legal = django_filters.CharFilter(field_name='legal__abbreviatedname', lookup_expr='contains')
    individual = django_filters.CharFilter(field_name='individual__name__last_name', lookup_expr='contains')
    address = django_filters.CharFilter(field_name='address', lookup_expr='contains')

    class Meta:
        model = Card
        fields = ['status', 'account', 'individual', 'legal', 'object_name', 'address',]

class CardDeviceForm(forms.ModelForm):
    class Meta:
        model = Card
        exclude =()
        fields = ('device',)

class CardQteamForm(forms.ModelForm):
    class Meta:
        model = Card
        exclude =()
        fields = ('qteam',)
'''
DeviceFormset=inlineformset_factory(Device, Sim, form=DeviceForm, extra=1)
CardDeviceFormset=inlineformset_factory(Card, Device, form=CardDeviceForm, extra=1)
CardQteamFormset=inlineformset_factory(Card, Responseteam, form=CardQteamForm, extra=1)
'''
