from django.contrib import admin

from .models import (Application, Individual, Legal, Phone, Phonebook,
                     Responsible)


class PhonebookInline(admin.TabularInline):
    model = Phonebook
    min_num = 1
    extra = 0

@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ('type', 'phone')
    fields = ['type', 'phone']
    search_fields = ('phone',)

@admin.register(Responsible)
class ResponsibleAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'fathers_name')
    fields = ['last_name', 'first_name', 'fathers_name']
    search_fields = ('phone', 'last_name')
    inlines = [PhonebookInline]
    empty_value_display = '-пусто-'

@admin.register(Legal)
class LegalAdmin(admin.ModelAdmin):
    list_display = (
        'fullname',
        'abbreviatedname',
        'legaladdress',
        'postaladdress',
        'telephone',
        'inn', 'kpp',
        'payment',
        'correspondent',
        'bic',
        'bank',
        'bigboss',
    )
    fields = [
        'fullname',
        'abbreviatedname',
        'legaladdress',
        'postaladdress',
        'telephone',
        ('inn', 'kpp'),
        'payment',
        'correspondent',
        'bic',
        'bank',
        'bigboss',
    ]
    search_fields = ('abbreviatedname',)
    empty_value_display = '-пусто-'

@admin.register(Individual)
class IndividualAdmin(admin.ModelAdmin):
    list_display = ('name', 'num_pass', 'issued', 'date')
    fields = ['name', 'num_pass', 'issued', 'date']
    search_fields = ('name',)
    empty_value_display = '-пусто-'

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'status',
        'legal',
        'individual',
        'object_name',
        'address',
        'transmission',
        'note',
        'manager',
        'generated',
        )
    fields = [
        'status',
        'legal',
        'individual',
        'object_name',
        'address',
        'transmission',
        'note',
        'manager',
        'generated',
        ]
    search_fields = ('legal', 'individual', 'address',)
    empty_value_display = '-пусто-'
