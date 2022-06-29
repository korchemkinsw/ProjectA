from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
from django.contrib.auth import get_user_model
from django.forms.models import inlineformset_factory

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

class DateInput(forms.DateInput):
    input_type = 'date'

class OrderFormCreate(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ()
        fields = (
            'number',
            'firm',
            'action',
            'perday',
            'comment',
        )
        labels = {
            'number': 'Номер приказа',
            'firm': 'Организация',
            'action': 'Действие',
            'perday': 'Выполнить до',
            'comment': 'Комментарий',
        }

        widgets = {
            'perday': DateInput(),
        }
        
    def __init__(self, *args, **kwargs):
        super(OrderFormCreate, self).__init__(*args, **kwargs)
        self.fields['perday'].widget = AdminDateWidget()

class OrderFormUpdate(forms.ModelForm):
    
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

        widgets = {
            'perday': DateInput(),
        }
        

    def __init__(self, *args, **kwargs):
        super(OrderFormUpdate, self).__init__(*args, **kwargs)
        self.fields['perday'].widget = AdminDateWidget()

ContractorOrderFormset = inlineformset_factory(Order, ContractorsOrder, form=ContractorOrderForm, extra=1)
FileOrderFormset = inlineformset_factory(Order, FileOrder, form=FileOrderForm, extra=1)
