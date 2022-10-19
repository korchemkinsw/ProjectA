from dataclasses import fields

import django_filters
from django import forms
from django.forms.models import inlineformset_factory

from .models import Card, CardPhoto, Device, Partition, Sim, Zone


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        exclude = ()
        fields = ('account',)
        labels ={
            'account': 'Передаваемый номер',
        }

class DeviceUpdateForm(forms.ModelForm):
    class Meta:
        model = Device
        exclude = ()
        fields = ('device', 'note',)
        labels ={
            'device': 'Тип ППК',
            'note': 'примечание',
        }

class DeviceNoneForm(forms.ModelForm):
    class Meta:
        model = Device
        exclude = ()
        fields = ('none',)

class SimForm(forms.ModelForm):
    
    class Meta:
        model = Sim
        exclude =()
        fields = ('part_sim', 'iccid', 'msisdn', 'image')

class PartitionForm(forms.ModelForm):
    class Meta:
        model = Partition
        exclude =()
        fields = ('number', 'name',)

class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        exclude =()
        fields = ('device', 'number', 'partition', 'name',)

class CardFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Card.STATUS_CHOICES)
    account = django_filters.CharFilter(field_name='device__account', lookup_expr='contains')
    legal = django_filters.CharFilter(field_name='legal__abbreviatedname', lookup_expr='contains')
    individual = django_filters.CharFilter(field_name='individual__name__last_name', lookup_expr='contains')
    object_name = django_filters.CharFilter(field_name='object_name', lookup_expr='contains')
    address = django_filters.CharFilter(field_name='address', lookup_expr='contains')

    class Meta:
        model = Card
        fields = ['status', 'account', 'individual', 'legal', 'object_name', 'address',]

class CardIndividualForm(forms.ModelForm):
    class Meta:
        model = Card
        exclude = ()
        fields = [
            'individual',
            'object_name',
            'address',
            'transmission',
            'note',
        ]

class CardLegalForm(forms.ModelForm):
    class Meta:
        model = Card
        exclude = ()
        fields = [
            'legal',
            'object_name',
            'address',
            'transmission',
            'note',
        ]

class CardDeviceForm(forms.ModelForm):
    class Meta:
        model = Card
        exclude = ()
        fields = ('device',)

class CardQteamForm(forms.ModelForm):
    class Meta:
        model = Card
        exclude = ()
        fields = ('contract', 'qteam', 'qnote')

class CardGPSForm(forms.ModelForm):
    class Meta:
        model = Card
        exclude = ()
        fields = ('address', 'width', 'longitude')

class CardPhotoForm(forms.ModelForm):
    class Meta:
        model = CardPhoto
        exclude = ()
        fields = ('title', 'image')

SimFormset=inlineformset_factory(Device, Sim, form=SimForm, extra=1)
PartitionFormset=inlineformset_factory(Device, Partition, form=PartitionForm, extra=1)
ZoneFormset=inlineformset_factory(Device, Zone, form=ZoneForm, extra=1)
PhotoFormset=inlineformset_factory(Card, CardPhoto, form=CardPhotoForm, extra=1)
