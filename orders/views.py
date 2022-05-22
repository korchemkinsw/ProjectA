from django.shortcuts import render
from Project_A import settings

from .models import ContractorsOrder, Order

def orders(request):
    orders = Order.objects.all()
    contractors = ContractorsOrder.objects.all()
    context={
        'my_company': settings.MYCOMPANY,
        'orders': orders,
        'contractors': contractors,
        'url': 'orders',
        }
    return render(request, "orders/orders.html", context)