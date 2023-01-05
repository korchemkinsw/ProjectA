from django.contrib import admin

from .models import CommentOrder, FileOrder, Order
from . forms import OrderForm


class FilesOrderInline(admin.TabularInline):
    model = FileOrder
    min_num = 1
    extra = 0

class CommentsOrderInline(admin.TabularInline):
    model = CommentOrder
    min_num = 1
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    form = OrderForm
    list_display = (
        'number',
        'status',
        'generated',
        'firm',
        'action',
        'perday',
        'changed',
        'lastuser',
    )

    search_fields = ("company",)
    inlines = [FilesOrderInline, CommentsOrderInline]
    empty_value_display = "-пусто-"

admin.site.register(Order, OrderAdmin)
