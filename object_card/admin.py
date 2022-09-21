from django.contrib import admin

from .models import Card, Contract, Device, Partition, Zone


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('account', 'device', 'sim_first', 'sim_two', 'application')
    fields = ['account', 'device', 'sim_first', 'sim_two', 'application']
    search_fields = ('account',)
    empty_value_display = '-пусто-'

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('enterprise', 'number', 'qteam', 'application')
    fields = ['enterprise', 'number', 'qteam', 'application']
    search_fields = ('enterprise', 'number', 'qteam')
    empty_value_display = '-пусто-'

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('device', 'application', 'contract', 'enginer', 'generated')
    fields = ['device', 'application', 'contract', 'enginer', 'generated']
    search_fields = ('device', 'application',)
    empty_value_display = '-пусто-'

@admin.register(Partition)
class PartitionAdmin(admin.ModelAdmin):
    list_display = ('device', 'number', 'name')
    fields = ['device', 'number', 'name']
    search_fields = ('card',)
    empty_value_display = '-пусто-'

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('partition', 'number', 'name')
    fields = ['partition', 'number', 'name']
    search_fields = ('partition',)
    empty_value_display = '-пусто-'
