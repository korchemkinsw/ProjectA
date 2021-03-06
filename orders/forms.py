import django_filters
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth import get_user_model
from django.forms.models import inlineformset_factory

from .models import CommentOrder, ContractorsOrder, FileOrder, Order

User = get_user_model()

NEW = 'новый'
INWORK = 'в работе'
PENDING = 'ожидающий'
COMPLETED = 'завершен'
REDJECTED = 'отклонен'
EXPIRED = 'Просрочен!'

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

    def __init__(self, *args, **kwargs):
        super (ContractorOrderForm,self ).__init__(*args,**kwargs)
        self.fields['contractor'].queryset = User.objects.filter(role=User.ENGINEER)

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
        self.fields['perday'].widget=AdminDateWidget()

class OrderFormUpdate(forms.ModelForm):
    STATUS_CHOICES = (
        (INWORK, 'В работе'),
        (COMPLETED, 'Завершен'),
        (REDJECTED, 'Отклонен'),
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES)
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

        widgets = {'perday': DateInput(),}
        

    def __init__(self, *args, **kwargs):
        super(OrderFormUpdate, self).__init__(*args, **kwargs)
        self.fields['perday'].widget=AdminDateWidget()

class OrderFilter(django_filters.FilterSet):
    STATUS_CHOICES = (
        (NEW, 'Новый'),
        (INWORK, 'В работе'),
        #(PENDING, 'Ожидающий'),
        (COMPLETED, 'Завершен'),
        (REDJECTED, 'Отклонен'),
        (EXPIRED, 'Просрочен!')
    )
    number = django_filters.CharFilter(field_name='number', lookup_expr='contains')
    status = django_filters.ChoiceFilter(choices=STATUS_CHOICES)
    generated_gt = django_filters.DateFilter(
        field_name='generated',
        widget=DateInput(attrs={'type': 'date'}),
        lookup_expr='gt'
        )
    generated_lt = django_filters.DateFilter(
        field_name='generated',
        widget=DateInput(attrs={'type': 'date'}),
        lookup_expr='lt'
        )
    comment = django_filters.CharFilter(field_name='comment', lookup_expr='contains')

    class Meta:
        model = Order
        fields = ['number', 'status', 'generated_gt', 'generated_lt', 'comment']

class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 3,'cols': 70}))
    class Meta:
        model = CommentOrder
        fields = ('comment',)


ContractorOrderFormset = inlineformset_factory(Order, ContractorsOrder, form=ContractorOrderForm, extra=1)
#FileOrderFormset = inlineformset_factory(Order, FileOrder, form=FileOrderForm, extra=1)
