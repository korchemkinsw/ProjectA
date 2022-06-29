import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import ContractorOrderFormset, OrderFormCreate, OrderFormUpdate
from .models import FileOrder, Order


class ListOrders(ListView):
    model = Order
    context_object_name = 'orders'

class CreateOrder(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderFormCreate

class CreateContractorOrder(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderFormCreate
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
            
            self.object = form.save(commit=False)
            self.object.author = self.request.user
            self.object.created = datetime.datetime.today()
            self.object.status = 'Новый'
            self.object.lastuser = self.request.user
            self.object.changed = datetime.datetime.today()
            self.object = form.save()

            if contractors.is_valid():
                contractors.instance = self.object
                contractors.save()
        return super(CreateContractorOrder, self).form_valid(form)

class UpdateOrder(LoginRequiredMixin, UpdateView):
    model = Order
    success_url = reverse_lazy('order', 'pk')


class UpdateContractorOrder(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderFormUpdate
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
            self.object = form.save(commit=False)
            self.object.lastuser = self.request.user
            self.object.changed = datetime.datetime.today()
            self.object = form.save()

            if contractors.is_valid():
                contractors.instance = self.object
                contractors.save()
        return super(UpdateContractorOrder, self).form_valid(form)

class DeleteOrder(LoginRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('orders')

class DetailOrder(DetailView):
    model = Order

class CreateDocument(CreateView):
    model = FileOrder
    fields = ['file']

    def get_success_url(self):
       pk = self.kwargs["pk"]
       return reverse("order", kwargs={"pk": pk})

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.order = get_object_or_404(Order, id=self.kwargs['pk'])
            self.object = form.save()
        return super(CreateDocument, self).form_valid(form)
