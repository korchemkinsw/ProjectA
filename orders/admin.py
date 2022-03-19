from dataclasses import field
from django.contrib import admin

from .models import Order, ContractorsOrder, FilesOrder, FileOrder

class ContractorsOrderInline(admin.TabularInline):
    model = ContractorsOrder
    min_num = 1
    extra = 0

class FilesOrderInline(admin.TabularInline):
    model = FilesOrder
    min_num = 1
    extra = 0

class FileOrderAdmin(admin.ModelAdmin):
    field = ['id', 'file']

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "status",
        "lastuser",
        "firm",
        "action",
        "generated",
        "perday",
    )

    search_fields = ("company",)
    inlines = (ContractorsOrderInline, FilesOrderInline,)
    empty_value_display = "-пусто-"

admin.site.register(Order, OrderAdmin,)
admin.site.register(FileOrder, FileOrderAdmin)
