from msilib.schema import Class
from django.db import transaction
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.forms import modelformset_factory
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from Project_A import settings

from .forms import OrderForm, ContractorOrderForm, ContractorOrderFormset
from .models import ContractorsOrder, FilesOrder, Order


class ListOrders(ListView):
    model = Order
    context_object_name = 'orders'

class CreateOrder(CreateView):
    model = Order
    fields = [
        'number',
        'firm',
        'action',
        'status',
        'perday',
        'comment',
    ]

class CreateContractorOrder(CreateView):
    model = Order
    fields = [
        'number',
        'firm',
        'action',
        'status',
        'perday',
        'comment',
    ]
    success_url = reverse_lazy('orders')

    def get_context_data(self, **kwargs):
        data = super(CreateContractorOrder, self).get_context_data(**kwargs)
        if self.request.POST:
            data['contractors'] = ContractorOrderFormset(self.request.POST)
        else:
            data['contractors'] = ContractorOrderFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        contractors = context['contractors']
        with transaction.atomic():
            self.object = form.save()

            if contractors.is_valid():
                contractors.instance = self.object
                contractors.save()
        return super(CreateContractorOrder, self).form_valid(form)

class UpdateOrder(UpdateView):
    model = Order
    success_url = '/'
    fields = [
        'number',
        'firm',
        'action',
        'status',
        'perday',
        'comment',
    ]

class UpdateContractorOrder(UpdateView):
    model = Order
    fields = [
        'number',
        'firm',
        'action',
        'status',
        'perday',
        'comment',
    ]
    success_url = reverse_lazy('order', 'pk')
        
    def get_success_url(self):
       pk = self.kwargs["pk"]
       return reverse("order", kwargs={"pk": pk})

    def get_context_data(self, **kwargs):
        data = super(UpdateContractorOrder, self).get_context_data(**kwargs)
        if self.request.POST:
            data['contractors'] = ContractorOrderFormset(self.request.POST, instance=self.object)
        else:
            data['contractors'] = ContractorOrderFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        contractors = context['contractors']
        with transaction.atomic():
            self.object = form.save()

            if contractors.is_valid():
                contractors.instance = self.object
                contractors.save()
        return super(UpdateContractorOrder, self).form_valid(form)

class DeleteOrder(DeleteView):
    model = Order
    success_url = reverse_lazy('orders')

class DetailOrder(DetailView):
    model = Order

class CreateDocument(CreateView):
    model = FilesOrder
    fields = ['file']