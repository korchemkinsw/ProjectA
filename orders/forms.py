from django import forms
from django.contrib.auth import get_user_model
from django.forms.models import (BaseInlineFormSet, inlineformset_factory)

from .models import ContractorsOrder, FileOrder, Order

User = get_user_model()

class FileOrderForm(forms.ModelForm):
    class Meta:
        model = FileOrder
        exclude = ()
        fields = ('file', 'order',)

class ContractorOrderForm(forms.ModelForm):
    class Meta:
        model = ContractorsOrder
        exclude = ()
        fields = ('contractor',)

class OrderForm(forms.ModelForm):
    perday = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    comment = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Order
        exclude = ()
        fields = (
            'number',
            'firm',
            'action',
            'status',
            'perday',
            'comment',
        )
        labels = {
            'number': 'Номер приказа',
            'firm': 'Организация',
            'action': 'Действие',
            'status': 'Статус приказа',
            'perday': 'Выполнить до',
            'comment': 'Комментарий',
        }

ContractorOrderFormset = inlineformset_factory(Order, ContractorsOrder, form=ContractorOrderForm, extra=1)
FileOrderFormset = inlineformset_factory(Order, FileOrder, form=FileOrderForm, extra=1)