from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django_filters.views import FilterView

from .forms import (ContactForm, ContactFormset, IndividualForm,
                    ResponsibleFilter)
from .models import Application, Individual, Legal, Responsible


class FilterContact(FilterView):
    model = Responsible
    context_object_name = 'filter'
    template_name = 'clientele/responsible_filter.html'
    filterset_class = ResponsibleFilter
    paginate_by = 5

class CreateContact(CreateView):
    model = Responsible
    form_class = ContactForm
    template_name = 'clientele/contacts_form.html'
    success_url = reverse_lazy('contactlist')

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

class ListLegal(ListView):
    model = Legal

class ListIndividual(ListView):
    model = Individual

class CreateIndividual(CreateView):
    model = Individual
    form_class = IndividualForm
    success_url = reverse_lazy('individual')

    def get_context_data(self, **kwargs):
        if 'individual' not in kwargs:
            kwargs['individual'] = get_object_or_404(Responsible, id=self.kwargs['pk'])
        return super().get_context_data(**kwargs)
        
    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.name = get_object_or_404(Responsible, id=self.kwargs['pk'])
            self.object = form.save()
        return super(CreateIndividual, self).form_valid(form)

class DetailIndividual(DetailView):
    model = Individual

