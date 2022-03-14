from django.contrib import admin

from .models import Enterprise

class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ("pk", "company", "bigboss",)
    search_fields = ("company",)
    empty_value_display = "-пусто-"

admin.site.register(Enterprise, EnterpriseAdmin)
