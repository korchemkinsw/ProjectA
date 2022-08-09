from django.contrib import admin

from .models import Enterprise, Position, Staffer


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

@admin.register(Staffer)
class StafferAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'fathers_name', 'post')
    fields = ['last_name', 'first_name', 'fathers_name', 'post']
