import datetime

from dal import autocomplete
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django_filters.views import FilterView
from enterprises.models import Enterprise

from .forms import (ContactFilter, ContactForm, ContactFormset, ContractFilter,
                    ContractForm, ContractFormset, IndividualFilter,
                    IndividualForm, LegalFilter, LegalForm)
from .models import Contract, Individual, Legal, Responsible


class EnterpriseAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Enterprise.objects.none()
        qs = Enterprise.objects.all()
        if self.q:
            qs = qs.filter(fullname__icontains=self.q)
        return qs

class FilterContact(FilterView):
    model = Responsible
    context_object_name = 'filter'
    template_name = 'clientele/responsible_filter.html'
    filterset_class = ContactFilter
    paginate_by = 5

class CreateContact(UserPassesTestMixin, CreateView):
    model = Responsible
    form_class = ContactForm
    template_name = 'clientele/contacts_form.html'
    success_url = reverse_lazy('contactlist')

    def test_func(self):
        if self.request.user.role == 'manager':
            return self.request.user.role == 'manager'
        return self.request.user.role == 'admin'

    def get_context_data(self, **kwargs):
        data = super(CreateContact, self).get_context_data(**kwargs)
        if self.request.POST:
            data['contacts'] = ContactFormset(self.request.POST)
        else:
            data['contacts'] = ContactFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        phones = context['contacts']
        if phones.is_valid():
            response = super(CreateContact, self).form_valid(form)
            phones.instance = self.object
            phones.save()
            return response
        else:
            return super().form_invalid(form)

class DetailContact(DetailView):
    model = Responsible

class FilterIndividual(FilterView):
    model = Individual
    context_object_name = 'filter'
    template_name = 'clientele/individual_filter.html'
    filterset_class = IndividualFilter
    paginate_by = 15

class CreateIndividual(UserPassesTestMixin, CreateView):
    model = Individual
    form_class = IndividualForm
    success_url = reverse_lazy('individual')

    def test_func(self):
        if self.request.user.role in ('manager', 'admin'):
            return True
        return False

    def get_context_data(self, **kwargs):
        if 'individual' not in kwargs:
            kwargs['individual'] = get_object_or_404(Responsible, id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        return context
        
    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.name = get_object_or_404(Responsible, id=self.kwargs['pk'])
            self.object = form.save()
        return super(CreateIndividual, self).form_valid(form)

class DetailIndividual(DetailView):
    model = Individual

class FilterLegal(FilterView):
    model = Legal
    context_object_name = 'filter'
    template_name = 'clientele/legal_filter.html'
    filterset_class = LegalFilter
    paginate_by = 15

class CreateLegal(UserPassesTestMixin, CreateView):
    model = Legal
    form_class = LegalForm
    success_url = reverse_lazy('legals')

    def test_func(self):
        if self.request.user.role in ('manager', 'admin'):
            return True
        return False

    def get_context_data(self, **kwargs):
        if 'legal' not in kwargs:
            kwargs['legal'] = get_object_or_404(Responsible, id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['form'].fields['bigboss'].queryset = Responsible.objects.filter(id=self.kwargs['pk'])
        return context
        
    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object = form.save()
        return super(CreateLegal, self).form_valid(form)

class DetailLegal(DetailView):
    model = Legal

class FilterContract(FilterView):
    model = Contract
    context_object_name = 'filter'
    template_name = 'clientele/contract_filter.html'
    filterset_class = ContractFilter
    paginate_by = 15

class DetailContract(DetailView):
    model = Contract

class CreateContractLegal(UserPassesTestMixin, CreateView):
    model = Contract
    form_class = ContractForm
    template_name = 'clientele\contract_form.html'

    def test_func(self):
        if self.request.user.role in ('director', 'admin'):
            return True
        return False

    def get_success_url(self):
       pk = self.kwargs['pk']
       return reverse('legal', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        data = super(CreateContractLegal, self).get_context_data(**kwargs)
        if self.request.POST:
            data['files'] = ContractFormset(self.request.POST, self.request.FILES)
        else:
            data['files'] = ContractFormset()
        data['title'] = 'Добавить договор'
        data['header'] = 'Добавить договор с '+str(get_object_or_404(Legal, id=self.kwargs['pk']).fullname)
        return data

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        files = context['files']
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.legal = get_object_or_404(Legal, id=self.kwargs['pk'])
            self.object = form.save()
            if files.is_valid():
                files.instance=self.object
                files.save()
        return super(CreateContractLegal, self).form_valid(form)

class UpdateContractLegal(UserPassesTestMixin, UpdateView):
    model = Contract
    form_class = ContractForm
    template_name = 'clientele\contract_form.html'

    def test_func(self):
        if self.request.user.role in ('director', 'admin'):
            return True
        return False

    def get_success_url(self):
       pk = self.kwargs['pk']
       return reverse('legal', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        data = super(UpdateContractLegal, self).get_context_data(**kwargs)
        contract = get_object_or_404(Contract, id=self.kwargs['pk'])
        if self.request.POST:
            data['files'] = ContractFormset(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['files'] = ContractFormset(instance=self.object)
        data['title'] = 'Изменить договор'
        data['header'] = 'Изменить договор с '+str(contract.legal.fullname)
        return data

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        files = context['files']
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object = form.save()
            if files.is_valid():
                files.instance=self.object
                files.save()
        return super(UpdateContractLegal, self).form_valid(form)

class CreateContractIndividual(UserPassesTestMixin, CreateView):
    model = Contract
    form_class = ContractForm
    template_name = 'clientele\contract_form.html'

    def test_func(self):
        if self.request.user.role in ('director', 'admin'):
            return True
        return False

    def get_success_url(self):
       pk = self.kwargs['pk']
       return reverse('individ', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        data = super(CreateContractIndividual, self).get_context_data(**kwargs)
        if self.request.POST:
            data['files'] = ContractFormset(self.request.POST, self.request.FILES)
        else:
            data['files'] = ContractFormset()
        data['title'] = 'Добавить договор'
        data['header'] = 'Добавить договор с '+str(get_object_or_404(Individual, id=self.kwargs['pk']).name)
        return data

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        files = context['files']
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.individual = get_object_or_404(Individual, id=self.kwargs['pk'])
            self.object = form.save()
            if files.is_valid():
                files.instance=self.object
                files.save()
        return super(CreateContractIndividual, self).form_valid(form)

class UpdateContractIndividual(UserPassesTestMixin, UpdateView):
    model = Contract
    form_class = ContractForm
    template_name = 'clientele/contract_form.html'

    def test_func(self):
        if self.request.user.role in ('director', 'admin'):
            return True
        return False

    def get_success_url(self):
       pk = self.kwargs['pk']
       return reverse('contract', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        data = super(UpdateContractIndividual, self).get_context_data(**kwargs)
        contract = get_object_or_404(Contract, id=self.kwargs['pk'])
        if self.request.POST:
            data['files'] = ContractFormset(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['files'] = ContractFormset(instance=self.object)
        data['title'] = 'Изменить договор'
        data['header'] = 'Изменить договор с '+str(contract.individual)
        return data

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        files = context['files']
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object = form.save()
            if files.is_valid():
                files.instance=self.object
                files.save()
        return super(UpdateContractIndividual, self).form_valid(form)
