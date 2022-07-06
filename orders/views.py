import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from users.models import CustomUser

from .forms import (CommentForm, ContractorOrderFormset, OrderFilter,
                    OrderFormCreate, OrderFormUpdate)
from .models import CommentOrder, FileOrder, Order


class ListOrders(LoginRequiredMixin, ListView):
    model = Order
    filterset_class = OrderFilter
    filterset_fields = ('number',)
    context_object_name = 'orders'
    
    def get_queryset(self):
        if self.request.user.role == CustomUser.ENGINEER:
            return Order.objects.filter(
                contractor=self.request.user
                ).exclude(
                    status=Order.COMPLETED
                    )
        if self.request.user.role == CustomUser.SECRETARY:
            return Order.objects.filter(
                author=self.request.user
                ).exclude(
                    status=Order.COMPLETED
                    )
        if self.request.user.role == CustomUser.ADMIN:
            return Order.objects.all()

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
    
    def get_success_url(self):
       pk = self.kwargs['pk']
       return reverse('order', kwargs={'pk': pk})

class UpdateContractorOrder(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderFormUpdate

    def get_success_url(self):
       pk = self.kwargs['pk']
       return reverse('order', kwargs={'pk': pk})

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
       pk = self.kwargs['pk']
       return reverse('order', kwargs={'pk': pk})

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.order = get_object_or_404(Order, id=self.kwargs['pk'])
            self.object = form.save()
        return super(CreateDocument, self).form_valid(form)

class DeleteDocument(DeleteView):
    model = FileOrder
    fields = ['file']

    def get_success_url(self):
       file = get_object_or_404(FileOrder, id=self.kwargs['pk'])
       return reverse('order', kwargs={'pk':file.order.id})

class CreateComment(CreateView):
    model = CommentOrder
    form_class = CommentForm
    
    def get_success_url(self):
       pk = self.kwargs['pk']
       return reverse('order', kwargs={'pk': pk})

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.order = get_object_or_404(Order, id=self.kwargs['pk'])
            self.object.created = datetime.datetime.today()
            self.object.author = self.request.user
            self.object = form.save()
        return super(CreateComment, self).form_valid(form)

def order_list(request):
    f = OrderFilter(request.GET, queryset=Order.objects.all())
    return render(request, 'orders/order_filter.html', {'filter': f})
