import django_filters
from dal import autocomplete
from django import forms
from django.forms.models import inlineformset_factory

from .models import (GPS, Card, CardPhoto, Device, Partition, Person, Qteam,
                     Sim, Zone)


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        exclude = ()
        fields = ('account','device', 'note',)
        labels ={
            'account': 'Передаваемый номер',
            'device': 'Тип ППК',
            'note': 'примечание',
        }
        widgets = {
            'note': forms.Textarea(attrs={'rows': 2,'cols': 65}),
            'device': autocomplete.ModelSelect2(url='type-autocomplete', attrs={'style': 'width:250px'}),
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
        exclude = ()
        fields = ('part_sim', 'iccid', 'msisdn', 'image')

class QteamForm(forms.ModelForm):
    class Meta:
        model = Qteam
        exclude = ()
        fields = ('qteam', 'type')
        widgets = {'qteam': autocomplete.ModelSelect2(url='qteam-autocomplete'),}

class GPSForm(forms.ModelForm):
    class Meta:
        model = GPS
        exclude = ()
        fields = ('gps',)

class PartitionForm(forms.ModelForm):
    class Meta:
        model = Partition
        exclude =()
        fields = ('number', 'name',)
        widgets = {
            'number': forms.NumberInput(attrs={'style': 'width:50px'}),
            'name': forms.TextInput(attrs={'style': 'width:750px'}),
            }

class ZoneForm(forms.ModelForm):
    def clean_device(self):
        data = self.cleaned_data['device']
        return data

    class Meta:
        model = Zone
        exclude =()
        fields = ('device', 'number', 'partition', 'name',)
        widgets = {
            'number': forms.NumberInput(attrs={'style': 'width:50px'}),
            'name': forms.TextInput(attrs={'style': 'width:550px'}),
            }

    def __init__(self, *args, **kwargs):
            super(ZoneForm, self).__init__(*args, **kwargs)
            #self.fields['partition'].queryset = Partition.objects.filter(device=self.fields['device'].instance)

class CardFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Card.STATUS_CHOICES)
    account = django_filters.CharFilter(field_name='object_key', lookup_expr='contains')
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
            'phone',
            'transmission',
            'note',
        ]
        widgets = {
            'object_name': forms.TextInput(attrs={'style': 'width:450px'}),
            'address': forms.TextInput(attrs={'style': 'width:450px'}),
            'phone': forms.TextInput(attrs={'style': 'width:450px'}),
            'note': forms.Textarea(attrs={'rows': 2,'cols': 65})
        }

class CardLegalForm(forms.ModelForm):
    class Meta:
        model = Card
        exclude = ()
        fields = [
            'legal',
            'object_name',
            'address',
            'phone',
            'transmission',
            'note',
        ]
        widgets = {
            'object_name': forms.TextInput(attrs={'style': 'width:450px'}),
            'address': forms.TextInput(attrs={'style': 'width:450px'}),
            'phone': forms.TextInput(attrs={'style': 'width:450px'}),
            'note': forms.Textarea(attrs={'rows': 2,'cols': 65})
        }

class CardDeviceForm(forms.ModelForm):
    class Meta:
        model = Card
        exclude = ()
        fields = ('device',)

class CardQnoteForm(forms.ModelForm):
    class Meta:
        model = Card
        exclude = ()
        fields = ('qnote',)
        widgets = {
            'qnote': forms.Textarea(attrs={'rows': 4,'cols': 65})
        }

class CardContractForm(forms.ModelForm):
    class Meta:
        model = Card
        exclude = ()
        fields = ('contract',)

class CardGPSForm(forms.ModelForm):
    class Meta:
        model = Card
        exclude = ()
        fields = ('none',)

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude =()
        fields = ('number', 'person', 'note', 'application')
        widgets = {
            'number': forms.NumberInput(attrs={'style': 'width:50px'}),
            'person': autocomplete.ModelSelect2(
                url='person-autocomplete',
                attrs={'style':'width:400px'}
                ),
            }

class CardPhotoForm(forms.ModelForm):
    class Meta:
        model = CardPhoto
        exclude = ()
        fields = ('title', 'image')

SimFormset=inlineformset_factory(Device, Sim, form=SimForm, extra=1)
PartitionFormset=inlineformset_factory(Device, Partition, form=PartitionForm, extra=1)
ZoneFormset=inlineformset_factory(Device, Zone, form=ZoneForm, extra=1)
PhotoFormset=inlineformset_factory(Card, CardPhoto, form=CardPhotoForm, extra=1)
