from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from Project_A import settings

from .forms import OrderForm
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

def new_order(request):
    form = OrderForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(
            request, 'orders/new_order.html', {'form': form})
                #'exp_action': 'new_order'
            
    new_order = form.save(commit=False)
    new_order.lastuser = request.user
    new_order.save()
    return redirect('orders')

class NewOrder(CreateView):
    form_class = OrderForm
    template_name = 'orders/new_order.html'
    success_url = reverse_lazy('orders')

