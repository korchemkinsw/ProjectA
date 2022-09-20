import django_filters
from django import forms
from django.forms.models import BaseInlineFormSet, inlineformset_factory

from .models import Card, Contract, Device, Partition, Zone


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        exclude = ()
        fields = ('account', 'device', 'sim_first', 'sim_two',)

class CardDevForm(forms.ModelForm):
    class Meta:
        model = Card
        exclude = ()
        fields = ('device', 'application',)
