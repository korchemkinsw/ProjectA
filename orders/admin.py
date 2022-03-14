from django.contrib import admin

from .models import Order

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
    empty_value_display = "-пусто-"

admin.site.register(Order, OrderAdmin)
