from django import forms
from django.forms.models import BaseInlineFormSet
from django.forms.models import inlineformset_factory, formset_factory
from django.contrib.auth import get_user_model

from .models import ContractorsOrder, FilesOrder, FileOrder, Order

User = get_user_model()

class FileOrderForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True})) 
    class Meta:
        model = FileOrder
        exclude = ()
        fields = ('file',)

class ContractorOrderForm(forms.ModelForm):
    class Meta:
        model = ContractorsOrder
        exclude = ()
        fields = ('contractor',)

class OrderForm(forms.ModelForm): 
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
#FileOrderFormset = inlineformset_factory(Order, FilesOrder, form=FileOrderForm, extra=0)

