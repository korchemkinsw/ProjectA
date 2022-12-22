from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .forms import ContractForm
from .models import (Phone, Contract, FileContract, Individual, Legal,
                     Contact)


class ContactPhonesInline(admin.TabularInline):
    model = Phone
    min_num = 1
    extra = 0

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ['name',]
    search_fields = ('name',)
    inlines = [ContactPhonesInline]
    empty_value_display = '-пусто-'

@admin.register(Legal)
class LegalAdmin(SimpleHistoryAdmin):
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
class IndividualAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'num_pass', 'issued', 'date')
    fields = ['name', 'num_pass', 'issued', 'date']
    search_fields = ('name',)
    empty_value_display = '-пусто-'

class ContractFilesInline(admin.TabularInline):
    model = FileContract
    min_num = 1
    extra = 0

@admin.register(Contract)
class ContractAdmin(SimpleHistoryAdmin):
    form = ContractForm
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
    inlines = [ContractFilesInline]
