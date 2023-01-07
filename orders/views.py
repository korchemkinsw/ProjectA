import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView
from users.models import CustomUser

from .forms import CommentForm, FileOrderFormset, OrderFilter, OrderForm
from .models import CommentOrder, Order


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

class CreateContractorOrder(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('orders')

    def get_context_data(self, **kwargs):
        data = super(CreateContractorOrder, self).get_context_data(**kwargs)
        if self.request.POST:
            data['files'] = FileOrderFormset(self.request.POST, self.request.FILES)
        else:
            data['files'] = FileOrderFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        files = context['files']
        with transaction.atomic():
            
            self.object = form.save(commit=False)
            self.object.author = self.request.user
            self.object.created = datetime.datetime.today()
            self.object.status = Order.NEW
            self.object.lastuser = self.request.user
            self.object.changed = datetime.datetime.today()
            self.object = form.save()

            if files.is_valid():
                files.instance = self.object
                files.save()
        return super(CreateContractorOrder, self).form_valid(form)

class UpdateContractorOrder(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm

    def get_success_url(self):
       pk = self.kwargs['pk']
       return reverse('order', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        NEW = 'новый'
        INWORK = 'в работе'
        PENDING = 'ожидающий'
        COMPLETED = 'завершен'
        REDJECTED = 'отклонен'
        EXPIRED = 'Просрочен!'

        STATUS_CHOICES = (
            (INWORK, 'В работе'),
            (COMPLETED, 'Завершен'),
            (REDJECTED, 'Отклонен'),
        )
        data = super(UpdateContractorOrder, self).get_context_data(**kwargs)
        data['form'].fields['status'].widget.choices = STATUS_CHOICES
        if self.request.POST:
            data['files'] = FileOrderFormset(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['files'] = FileOrderFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        files = context['files']
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.lastuser = self.request.user
            self.object.changed = datetime.datetime.today()
            #if self.object.author == self.request.user:
            #    self.object.status = 'Новый'
            self.object = form.save()

            if files.is_valid():
                files.instance = self.object
                files.save()
        return super(UpdateContractorOrder, self).form_valid(form)

class DeleteOrder(LoginRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('orders')

class DetailOrder(DetailView):
    model = Order

class CreateComment(CreateView):
    model = CommentOrder
    form_class = CommentForm
    template_name = 'orders/order_detail.html'
    
    def get_success_url(self):
       pk = self.kwargs['pk']
       return reverse('order', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        data = super(CreateComment, self).get_context_data(**kwargs)
        data['order'] = get_object_or_404(Order, id=self.kwargs['pk'])
        data['action'] = 'create_comment'
        return data

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.order = get_object_or_404(Order, id=self.kwargs['pk'])
            self.object.created = datetime.datetime.today()
            self.object.author = self.request.user
            self.object = form.save()
        return super(CreateComment, self).form_valid(form)
