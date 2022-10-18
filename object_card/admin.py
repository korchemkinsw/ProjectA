from django.contrib import admin

from .models import Card, CardPhoto, Device, ImageSim, Partition, Sim, Zone


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        'account', 'device', 'enginer_pult',
        'changed_pult', 'technican', 'changed_tech'
        )
    fields = [
        'account', 'device', 'enginer_pult',
        'changed_pult', 'technican', 'changed_tech'
        ]
    search_fields = ('account',)
    empty_value_display = '-пусто-'

@admin.register(Sim)
class SimAdmin(admin.ModelAdmin):
    list_display = ('device', 'part_sim', 'iccid', 'msisdn', 'image')
    fields = ['device', 'part_sim', 'iccid', 'msisdn', 'image']
    search_fields = ('iccid', 'msisdn', 'device',)
    empty_value_display = '-пусто-'
'''
@admin.register(ImageSim)
class ImageSimAdmin(admin.ModelAdmin):
    list_display = ('device', 'part_sim', 'image')
    fields = ['device', 'part_sim', 'image']
    search_fields = ('device', 'part_sim',)
    empty_value_display = '-пусто-'
'''
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = (
        'status', 'legal', 'individual', 'object_name',
        'phone', 'address', 'width', 'longitude',
        'transmission', 'device', 'note', 'contract', 'qteam', 'qnote',
        'manager', 'generated', 'director', 'changed'
        )
    fields = [
        'status', 'legal', 'individual', 'object_name',
        'phone', 'address', 'width', 'longitude',
        'transmission', 'device', 'note', 'contract', 'qteam', 'qnote',
        'manager', 'generated', 'director', 'changed'
        ]
    search_fields = ('device', 'legal', 'individual', 'address',)
    empty_value_display = '-пусто-'

@admin.register(Partition)
class PartitionAdmin(admin.ModelAdmin):
    list_display = ('device', 'number', 'name')
    fields = ['device', 'number', 'name']
    search_fields = ('device',)
    empty_value_display = '-пусто-'

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
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
