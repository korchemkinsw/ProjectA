import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView
from users.models import CustomUser

from .forms import (CommentForm, ContractorOrderFormset, OrderFilter,
                    OrderFormCreate, OrderFormUpdate)
from .models import CommentOrder, FileOrder, Order


class ListOrders(LoginRequiredMixin, FilterView):
    model = Order
    context_object_name = 'filter'
    template_name = 'orders/order_filter.html'
    filterset_class = OrderFilter
    paginate_by = 5

    def get_queryset(self):
        expireds = Order.objects.filter(perday__lt=datetime.date.today()).exclude(status='завершен')
        for expired in expireds:
            expired.status = 'Просрочен!'
            expired.save()
        if self.request.user.role == CustomUser.ENGINEER:
            return Order.objects.filter(
                contractor=self.request.user
                ).exclude(status='завершен').order_by('perday')
        if self.request.user.role == CustomUser.SECRETARY:
            return Order.objects.filter(
                author=self.request.user
                ).exclude()
        if self.request.user.role == CustomUser.ADMIN:
            return Order.objects.all()
    
    def get_context_data(self, *args, **kwargs):
        _request_copy = self.request.GET.copy()
        parameters = _request_copy.pop('page', True) and _request_copy.urlencode()
        context = super().get_context_data(*args, **kwargs)
        context['parameters'] = parameters
        return context

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
            self.object.status = Order.NEW
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
            if self.object.author == self.request.user:
                self.object.status = 'Новый'
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
