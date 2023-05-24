from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import GuardObject, GuardPost, GuardsOnDuty, WorkingShift


class GuardsOnDutyInline(admin.TabularInline):
    model = GuardsOnDuty
    min_num = 0
    extra = 0

class WorkingShiftInline(admin.TabularInline):
    model = WorkingShift
    min_num = 0
    extra = 0

@admin.register(GuardObject)
class GuardObjectAdmin(admin.ModelAdmin):
    list_display = ('pk', 'contract', 'qteam', 'number')
    fields = ['contract', 'qteam', 'number']
    sreash_fields = ('contract', 'qteam')
    empty_value_display = '-пусто-'

@admin.register(GuardPost)
class GuardPostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'guard_object', 'number', 'note',)
    fields = ['guard_object', 'number', 'note',]
    sreash_fields = ('guard_object', 'number', 'note')
    inlines = [GuardsOnDutyInline]
    empty_value_display = '-пусто-'

@admin.register(WorkingShift)
class WorkingShiftAdmin(admin.ModelAdmin):
    list_display = ('pk', 'security', 'shift', 'begin', 'end')
    fields = ['security', 'shift', 'begin', 'end']
    sreash_fields = ('security', 'shift', 'begin', 'end')
    empty_value_display = '-пусто-'

@admin.register(GuardsOnDuty)
class GuardsOnDutyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'post', 'security')
    fields = ['post', 'security']
    sreash_fields = ('post', 'security')
    empty_value_display = '-пусто-'