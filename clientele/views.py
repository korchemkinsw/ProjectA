from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import ContactForm, PhoneForm, PhoneFormset, ResponsibleForm
from .models import (Application, Individual, Legal, Phone, Phonebook,
                     Responsible)


class ListResponsible(ListView):
    model = Responsible

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
        context = self.get_context_data()
        phones = context['phonebook']
        with transaction.atomic():
            
            self.object = form.save(commit=False)
            self.object = form.save()

            if phones.is_valid():
                phones.instance = self.object
                phones.save()
        return super(CreateContact, self).form_valid(form)

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
