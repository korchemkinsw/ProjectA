from dataclasses import field

from django.contrib import admin

from .models import ContractorsOrder, FileOrder, Order


class ContractorsOrderInline(admin.TabularInline):
    model = ContractorsOrder
    min_num = 1
    extra = 0

class FileOrderAdmin(admin.ModelAdmin):
    field = ['order', 'file']

class ContractorOrderAdmin(admin.ModelAdmin):
    field = ['order', 'contractor']

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'number',
        'firm',
        'action',
        'status',
        'perday',
    )

    search_fields = ("company",)
    inlines = [ContractorsOrderInline]
    empty_value_display = "-пусто-"

admin.site.register(Order, OrderAdmin,)
admin.site.register(FileOrder, FileOrderAdmin)
admin.site.register(ContractorsOrder, ContractorOrderAdmin)
