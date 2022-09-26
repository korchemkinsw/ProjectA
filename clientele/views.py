import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django_filters.views import FilterView
from object_card.models import Card

from .forms import (AppIndividualForm, AppLegalForm, ContactFilter,
                    ContactForm, ContactFormset, IndividualForm, LegalForm)
from .models import Individual, Legal, Responsible


class FilterContact(FilterView):
    model = Responsible
    context_object_name = 'filter'
    template_name = 'clientele/responsible_filter.html'
    filterset_class = ContactFilter
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

class ListIndividual(ListView):
    model = Individual

class CreateIndividual(CreateView):
    model = Individual
    form_class = IndividualForm
    success_url = reverse_lazy('individual')

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

class ListLegal(ListView):
    model = Legal

class CreateLegal(CreateView):
    model = Legal
    form_class = LegalForm
    success_url = reverse_lazy('legals')

    def get_context_data(self, **kwargs):
        if 'legal' not in kwargs:
            kwargs['legal'] = get_object_or_404(Responsible, id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['form'].fields['bigboss'].queryset = Responsible.objects.filter(id=self.kwargs['pk'])
        return context
        
    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            #self.object.bigboss = get_object_or_404(Responsible, id=self.kwargs['pk'])
            self.object = form.save()
        return super(CreateLegal, self).form_valid(form)

class DetailLegal(DetailView):
    model = Legal

class ListApplication(ListView):
    model = Card

class CreateAppIndividual(CreateView):
    model = Card
    form_class = AppIndividualForm
    template_name = 'form.html'
    success_url = reverse_lazy('individual')

    def get_context_data(self, **kwargs):
        if 'application' not in kwargs:
            kwargs['application'] = get_object_or_404(Individual, id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['form'].fields['individual'].queryset = Individual.objects.filter(id=self.kwargs['pk'])
        context['client']=kwargs['application'].name
        return context

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.status = Card.NEW
            self.object.manager = self.request.user
            self.object.generated = datetime.datetime.today()
            self.object = form.save()
        return super(CreateAppIndividual, self).form_valid(form)

class CreateAppLegal(CreateView):
    model = Card
    form_class = AppLegalForm
    template_name = 'form.html'
    success_url = reverse_lazy('legals')

    def get_context_data(self, **kwargs):
        if 'application' not in kwargs:
            kwargs['application'] = get_object_or_404(Legal, id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['form'].fields['legal'].queryset = Legal.objects.filter(id=self.kwargs['pk'])
        context['client']=kwargs['application'].abbreviatedname
        return context

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.status = Card.NEW
            self.object.manager = self.request.user
            self.object.generated = datetime.datetime.today()
            self.object = form.save()
        return super(CreateAppLegal, self).form_valid(form)

class DetailApplication(DetailView):
    model = Card
    