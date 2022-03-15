from django.contrib import admin

from .models import FilesOrder, Order, ContractorsOrder

class ContractorsOrderInline(admin.TabularInline):
    model = ContractorsOrder
    min_num = 1
    extra = 0

class FilesOrderInline(admin.TabularInline):
    model = FilesOrder
    #min_num = 1
    #extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "status",
        "lastuser",
        "firm",
        "action",
        "generated",
        "perday",
        #"contractor",
        "order",
    )

    search_fields = ("company",)
    inlines = (ContractorsOrderInline,)
    #inlines = (FilesOrderInline,)
    empty_value_display = "-пусто-"

admin.site.register(Order, OrderAdmin)
