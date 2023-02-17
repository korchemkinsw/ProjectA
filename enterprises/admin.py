from django.contrib import admin

from .forms import (PersonalCardForm, SecurityForm, WeaponForm,
                    WeaponsPermitForm)
from .models import (Enterprise, PersonalCard, Position, Responseteam,
                     Security, Weapon, WeaponsPermit, Worker)


@admin.register(Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
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

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'post')
    fields = ['post']
'''
@admin.register(Staffer)
class StafferAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'fathers_name', 'post')
    fields = ['last_name', 'first_name', 'fathers_name', 'post']
'''
@admin.register(Responseteam)
class ResponseteamAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')
    fields = ['name', 'phone']

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'post')
    fields = ['name', 'post']

class WeaponsPermitInline(admin.TabularInline):
    model = WeaponsPermit
    form = WeaponsPermitForm
    min_num = 0
    extra = 0

class PersonalCardInline(admin.TabularInline):
    model = PersonalCard
    form = PersonalCardForm
    min_num = 0
    extra = 0

@admin.register(Security)
class SecurityAdmin(admin.ModelAdmin):
    form = SecurityForm
    list_display = (
        'security', 'photo', 'epp', 'medical', 'category',
        'id_number', 'status', 'issue', 'prolonged', 'note'
        )
    fields = [
        'security', 'photo', 'epp', 'medical', 'category',
        'id_number', 'status', 'issue', 'prolonged', 'note'
        ]
    inlines = [WeaponsPermitInline, PersonalCardInline]

@admin.register(Weapon)
class WeaponAdmin(admin.ModelAdmin):
    form = WeaponForm
    list_display = ('model', 'caliber', 'series', 'number', 'release')
    fields = ['model', 'caliber', 'series', 'number', 'release']

@admin.register(WeaponsPermit)
class WeaponPermitAdmin(admin.ModelAdmin):
    form = WeaponsPermitForm
    list_display = ('series', 'number', 'security', 'enterprise', 'weapon', 'issue')
    fields = ['series', 'number', 'security', 'enterprise', 'weapon', 'issue']

@admin.register(PersonalCard)
class PersonalCardAdmin(admin.ModelAdmin):
    form = PersonalCardForm
    list_display = ('series', 'number', 'security', 'enterprise', 'type', 'issue')
    fields = ['series', 'number', 'security', 'enterprise', 'type', 'issue']