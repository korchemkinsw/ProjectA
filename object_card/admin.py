from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .forms import DeviceForm, GPSForm, PersonForm, QteamForm, ZoneForm
from .models import (GPS, Card, CardPhoto, Device, Partition, Person, Qteam,
                     Sim, Type_device, Zone)


class DeviceSimInline(admin.TabularInline):
    model = Sim
    min_num = 0
    extra = 0

class DevicePartitionInline(admin.TabularInline):
    model = Partition
    min_num = 0
    extra = 0

class DeviceZoneInline(admin.TabularInline):
    model = Zone
    form = ZoneForm
    min_num = 0
    extra = 0

@admin.register(Device)
class DeviceAdmin(SimpleHistoryAdmin):
    list_display = (
        'account', 'device', 'enginer_pult',
        'changed_pult', 'technican', 'changed_tech',
        )
    fields = [
        'account', 'device', 'enginer_pult',
        'changed_pult', 'technican', 'changed_tech',
        ]
    search_fields = ('account',)
    inlines = [DeviceSimInline, DevicePartitionInline, DeviceZoneInline]
    form = DeviceForm
    empty_value_display = '-пусто-'

class CardGPSInline(admin.TabularInline):
    model = GPS
    form = GPSForm
    min_num = 0
    max_num = 1
    extra = 1

class CardQteamInline(admin.TabularInline):
    model = Qteam
    form = QteamForm
    min_num = 0
    extra = 0

class CardPersonInline(admin.TabularInline):
    model = Person
    form = PersonForm
    min_num = 0
    extra = 0

class CardPhotoInline(admin.TabularInline):
    model = CardPhoto
    min_num = 0
    extra = 0

@admin.register(Type_device)
class Type_deviceAdmin(admin.ModelAdmin):
    list_display = ('transmission', 'device')
    fields = ['transmission', 'device']
    sreash_fields = ('transmission', 'device')
    empty_value_display = '-пусто-'

@admin.register(Card)
class CardAdmin(SimpleHistoryAdmin):
    list_display = (
        'status', 'object_key', 'legal', 'individual',
        'object_name', 'phone', 'address',
        'transmission', 'device', 'note', 'contract', 'qnote',
        'manager', 'generated', 'director', 'changed',
        )
    fields = [
        'status', 'object_key', 'legal', 'individual',
        'object_name', 'phone', 'address',
        'transmission', 'device', 'note', 'contract', 'qnote',
        'manager', 'generated', 'director', 'changed',
        ]
    search_fields = ('device', 'legal', 'individual', 'address',)
    inlines = [CardGPSInline, CardQteamInline, CardPersonInline, CardPhotoInline]
    empty_value_display = '-пусто-'
