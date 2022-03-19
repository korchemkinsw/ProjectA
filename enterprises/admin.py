from django.contrib import admin

from .models import Enterprise

class EnterpriseAdmin(admin.ModelAdmin):
    list_display = (
        "fullname",
        "abbreviatedname",
        "legaladdress",
        "postaladdress",
        "telephone",
        "inn", "kpp",
        "payment",
        "correspondent",
        "bic",
        "bank",
        "bigboss",
    )
    fields = [
        "fullname",
        "abbreviatedname",
        "legaladdress",
        "postaladdress",
        "telephone",
        ("inn", "kpp"),
        "payment",
        "correspondent",
        "bic",
        "bank",
        "bigboss",
    ]
    search_fields = ("abbreviatedname",)
    empty_value_display = "-пусто-"

admin.site.register(Enterprise, EnterpriseAdmin)
