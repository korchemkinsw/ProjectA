from django.contrib import admin

from .models import (Contact, Contract, FileContract, Individual, Legal,
                     Responsible)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('responsible', 'type', 'phone')
    fields = ['responsible', 'type', 'phone']
    search_fields = ('responsible', 'phone',)

@admin.register(Responsible)
class ResponsibleAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'fathers_name')
    fields = ['last_name', 'first_name', 'fathers_name']
    search_fields = ('last_name',)
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

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        'status',
        'number',
        'date',
        'enterprise',
        'legal',
        'individual',
        )
    fields = [
        'status',
        'number',
        'date',
        'enterprise',
        'legal',
        'individual',
        'contractholder',
        ]
    search_fields = ('number', 'date', 'enterprise',)

@admin.register(FileContract)
class FileContractAdmin(admin.ModelAdmin):
    list_display = ('contract', 'title', 'file', 'generated')
    field = ['contract', 'title', 'file', 'generated']

