from django import forms
from django.forms.models import BaseInlineFormSet
from django.forms.models import inlineformset_factory, formset_factory
from django.contrib.auth import get_user_model

from .models import ContractorsOrder, FileOrder, Order

User = get_user_model()

class FileOrderForm(forms.ModelForm):
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
            'status',
            'firm',
            'action',
            'perday',
            #'contractor',
            #'order',
        )
        labels = {
            'status': 'Статус приказа',
            'firm': 'Организация',
            'action': 'Действие',
            'perday': 'Выполнить до',
            #'contractor': 'Исполнители',
            #'order': 'Файлы',
        }
    #contractor=forms.ModelMultipleChoiceField(ContractorOrder.objects.all())
    #order=forms.ModelMultipleChoiceField(FileOrder.objects.all())

ContractorOrderFormset = inlineformset_factory(Order, ContractorsOrder, form=ContractorOrderForm, extra=0)
ContractorOrderFormset = inlineformset_factory(Order, ContractorsOrder, form=FileOrderForm, fields='__all__',min_num = 1,  extra=0)


'''
class BaseContractorFormset(BaseInlineFormSet):
    pass

ContractorFormset = inlineformset_factory(Order, ContractorOrder, formset=BaseContractorFormset, extra=1)
'''