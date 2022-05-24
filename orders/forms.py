from django import forms
from django.contrib.auth import get_user_model

from .models import ContractorsOrder, FileOrder, Order

User = get_user_model()

class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = (
            'status',
            'firm',
            'action',
            'perday',
            'contractor',
            #'order',
        )
        labels = {
            'status': 'Статус приказа',
            'firm': 'Организация',
            'action': 'Действие',
            'perday': 'Выполнить до',
            'contractor': 'Исполнители',
            'order': 'Файлы',
        }
    contractor=forms.ModelMultipleChoiceField(User.objects.all())

