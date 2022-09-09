from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django_filters.views import FilterView

from .forms import (ContactForm, ContactFormset, ContactsForm, PhoneForm,
                    PhoneFormset, ResponsibleFilter, ResponsibleForm)
from .models import (Application, Individual, Legal, Phone, Phonebook,
                     Responsible)


class ListResponsible(ListView):
    model = Responsible

class FilterContact(FilterView):
    model = Responsible
    context_object_name = 'filter'
    template_name = 'clientele/responsible_filter.html'
    filterset_class = ResponsibleFilter
    paginate_by = 5

class CreateContact(CreateView):
    model = Responsible
    form_class = ContactForm
    template_name = 'clientele/contact_form.html'
    success_url = reverse_lazy('responsible')

    def get_context_data(self, **kwargs):
        data = super(CreateContact, self).get_context_data(**kwargs)
        if self.request.POST:
            data['phonebook'] = PhoneFormset(self.request.POST)
        else:
            data['phonebook'] = PhoneFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        phones = context['phonebook']
        if phones.is_valid():
            response = super(CreateContact, self).form_valid(form)
            phones.instance = self.object
            phones.save()
            return response
        else:
            return super().form_invalid(form)

class CreateContacts(CreateView):
    model = Responsible
    form_class = ContactForm
    template_name = 'clientele/contacts_form.html'
    success_url = reverse_lazy('responsible')

    def get_context_data(self, **kwargs):
        data = super(CreateContacts, self).get_context_data(**kwargs)
        if self.request.POST:
            data['contacts'] = ContactFormset(self.request.POST)
        else:
            data['contacts'] = ContactFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        phones = context['contacts']
        if phones.is_valid():
            response = super(CreateContacts, self).form_valid(form)
            phones.instance = self.object
            phones.save()
            return response
        else:
            return super().form_invalid(form)

class CreateResponsible(CreateView):
    model = Responsible
    form_class = ResponsibleForm
    success_url = reverse_lazy('responsible')

class CreatePhone(CreateView):
    model = Phone
    form_class = PhoneForm
    success_url = reverse_lazy('add_responsible')

class ListLegal(ListView):
    model = Legal

class ListIndividual(ListView):
    model = Individual
