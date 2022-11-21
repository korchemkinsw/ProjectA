from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .forms import QteamForm
from .models import Card, CardPhoto, Device, Partition, Qteam, Sim, Zone


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
    empty_value_display = '-пусто-'

@admin.register(Sim)
class SimAdmin(SimpleHistoryAdmin):
    list_display = ('device', 'part_sim', 'iccid', 'msisdn', 'image')
    fields = ['device', 'part_sim', 'iccid', 'msisdn', 'image']
    search_fields = ('iccid', 'msisdn', 'device',)
    empty_value_display = '-пусто-'

@admin.register(Card)
class CardAdmin(SimpleHistoryAdmin):
    list_display = (
        'status', 'legal', 'individual', 'object_name',
        'phone', 'address', 'width', 'longitude',
        'transmission', 'device', 'note', 'contract', 'qnote',
        'manager', 'generated', 'director', 'changed',
        )
    fields = [
        'status', 'legal', 'individual', 'object_name',
        'phone', 'address', 'width', 'longitude',
        'transmission', 'device', 'note', 'contract', 'qnote',
        'manager', 'generated', 'director', 'changed',
        ]
    search_fields = ('device', 'legal', 'individual', 'address',)
    empty_value_display = '-пусто-'

@admin.register(Qteam)
class QteamAdmin(SimpleHistoryAdmin,):
    form = QteamForm
    list_display = ('id', 'card', 'type', 'qteam')
    fields = ['card', 'type', 'qteam']
    search_fields = ('card',)
    empty_value_display = '-пусто-'

@admin.register(Partition)
class PartitionAdmin(SimpleHistoryAdmin):
    list_display = ('device', 'number', 'name')
    fields = ['device', 'number', 'name']
    search_fields = ('device',)
    empty_value_display = '-пусто-'

@admin.register(Zone)
class ZoneAdmin(SimpleHistoryAdmin):
    list_display = ('device', 'partition', 'number', 'name')
    fields = ['device', 'partition', 'number', 'name']
    search_fields = ('device', 'partition',)
    empty_value_display = '-пусто-'

@admin.register(CardPhoto)
class CardPhotoAdmin(admin.ModelAdmin):
    list_display = ('card', 'title', 'image',)
    fields = ['card', 'title', 'image',]
    search_fields = ('card', 'title',)
    empty_value_display = '-пусто-'
