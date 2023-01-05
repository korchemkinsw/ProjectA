import django_filters
from django import forms
from django.contrib.auth import get_user_model
from django.forms.models import inlineformset_factory

from .models import CommentOrder, FileOrder, Order

User = get_user_model()

class FileOrderForm(forms.ModelForm):
    class Meta:
        model = FileOrder
        exclude = ()
        fields = ('file', 'order',)

class OrderForm(forms.ModelForm):
    contractor=forms.ModelMultipleChoiceField(
        label='Исполнители',
        queryset=User.objects.filter(role=User.ENGINEER),
        widget=forms.widgets.CheckboxSelectMultiple()
        )
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
            'comment': 'Пояснение',
        }

        widgets = {
            'perday': forms.TextInput(attrs={'class': 'vDateField', 'type': 'date'}),
            'comment': forms.Textarea(attrs={'rows': 2,'cols': 50})
        }
        
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
          self.fields['contractor'].initial = self.instance.contractor.all()

class OrderFilter(django_filters.FilterSet):
    NEW = 'новый'
    INWORK = 'в работе'
    PENDING = 'ожидающий'
    COMPLETED = 'завершен'
    REDJECTED = 'отклонен'
    EXPIRED = 'Просрочен!'
    STATUS_CHOICES = (
        (NEW, 'Новый'),
        (INWORK, 'В работе'),
        #(PENDING, 'Ожидающий'),
        (COMPLETED, 'Завершен'),
        (REDJECTED, 'Отклонен'),
        (EXPIRED, 'Просрочен!')
    )
    number = django_filters.CharFilter(
        field_name='number',
        widget=forms.TextInput(attrs={'style':'width:70px'}),
        lookup_expr='contains'
    )
    status = django_filters.ChoiceFilter(choices=STATUS_CHOICES)
    generated_gt = django_filters.DateFilter(
        field_name='generated',
        widget=forms.TextInput(attrs={'class': 'vDateField', 'type': 'date'}),
        lookup_expr='gt'
        )
    generated_lt = django_filters.DateFilter(
        field_name='generated',
        widget=forms.TextInput(attrs={'class': 'vDateField', 'type': 'date'}),
        lookup_expr='lte'
        )
    comment = django_filters.CharFilter(field_name='comment', lookup_expr='contains')

    class Meta:
        model = Order
        fields = ['number', 'status', 'generated_gt', 'generated_lt', 'comment']

class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 2,'cols': 50}))
    class Meta:
        model = CommentOrder
        fields = ('comment',)


FileOrderFormset = inlineformset_factory(Order, FileOrder, form=FileOrderForm, extra=1)
