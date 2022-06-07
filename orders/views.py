from msilib.schema import Class
from django.db import transaction
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.forms import modelformset_factory
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from Project_A import settings

from .forms import OrderForm, ContractorOrderForm, ContractorOrderFormset
from .models import ContractorsOrder, Order


class ListOrders(ListView):
    model = Order
    #template_name = 'orders/orders.html'
    context_object_name = 'orders'

class CreateOrder(CreateView):
    model = Order
    fields = [
        'status',
        'firm',
        'action',
        'perday',
    ]
    #template_name = 'orders/add_order.html'

class CreateContractorOrder(CreateView):
    model = Order
    fields = [
        'status',
        'firm',
        'action',
        'perday',
    ]
    #template_name = 'orders/add_order.html'
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
        'status',
        'firm',
        'action',
        'perday',
    ]

class UpdateContractorOrder(UpdateView):
    model = Order
    fields = [
        'status',
        'firm',
        'action',
        'perday',
    ]
    #template_name = 'orders/add_order.html'
    success_url = reverse_lazy('orders')

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

'''
class NewOrder(CreateView):
    form_class = OrderForm
    template_name = 'orders/add_order.html'
    model = Order
    success_url = '/'
    
    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        contractors = ContractorOrderFormset()

        return self.render_to_response(
            self.get_context_data(form=form, contractors=contractors)
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        contractor_form = ContractorOrderFormset(self.request.POST)

        if (form.is_valid() and contractor_form.is_valid()):
            return self.form_valid(form, contractor_form)

        return self.form_invalid(form, contractor_form)

    def form_valid(self, form, contractor_form):
        """
        Called if all forms are valid. Creates a Author instance along
        with associated books and then redirects to a success page.
        """
        self.object = form.save()
        contractor_form.instance = self.object
        contractor_form.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, contractor_form):
        """
        Called if whether a form is invalid. Re-renders the context
        data with the data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form, contractor_form=contractor_form)
        )

    def get_context_data(self, **kwargs):
        """ Add formset and formhelper to the context_data. """
        ctx = super(NewOrder, self).get_context_data(**kwargs)


        if self.request.POST:
            ctx['form'] = OrderForm(self.request.POST)
            ctx['contractor_form'] = ContractorOrderFormset(self.request.POST)
        else:
            ctx['form'] = OrderForm()
            ctx['contractor_form'] = ContractorOrderFormset()

        return ctx
    
    def get_context_data(self, **kwargs):
        data = super(NewOrder, self).get_context_data(**kwargs)
        if self.request.POST:
            data['contractors'] = ContractorOrderFormset(self.request.POST)
        else:
            data['contractors'] = ContractorOrderFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        contractor = context['contractors']
        with transaction.atomic():
            self.object = form.save()

            if contractor.is_valid():
                contractor.instance = self.object
                contractor.save()
        return super(NewOrder, self).form_valid(form)
        '''
