import datetime

from clientele.models import Individual, Legal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)
from django_filters.views import FilterView

from .forms import (CardFilter, CardIndividualForm, CardLegalForm,
                    CardQteamForm, DeviceForm, DevicePartForm,
                    PartitionFormset, SimFormset)
from .models import Card, Device, Partition, Zone


class FilterCard(FilterView):
    model = Card
    context_object_name = 'filter'
    template_name = 'object_card/card_filter.html'
    filterset_class = CardFilter
    paginate_by = 15

class DetailCard(DetailView):
    model = Card

class DetailCardDevice(DetailView):
    model = Card
    template_name = 'object_card\card_device_detail.html'

class DetailCardQteam(DetailView):
    model = Card
    template_name = 'object_card\card_qteam_detail.html'

class DetailCardPartitions(DetailView):
    model = Card
    template_name = 'object_card\card_partitions_detail.html'

class CreateCardIndividual(CreateView):
    model = Card
    form_class = CardIndividualForm
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
        return super(CreateCardIndividual, self).form_valid(form)

class CreateCardLegal(CreateView):
    model = Card
    form_class = CardLegalForm
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
        return super(CreateCardLegal, self).form_valid(form)

class UpdateCardQteam(UpdateView):
    model = Card
    form_class = CardQteamForm
    template_name = 'form.html'

    def get_success_url(self):
       pk = self.kwargs['pk']
       return reverse('card_qteam', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        data = super(UpdateCardQteam, self).get_context_data(**kwargs)
        data['card'] = get_object_or_404(Card, id=self.kwargs['pk'])
        data['title'] = 'Добавить реагирование'
        data['header'] = 'Добавить реагирование'
        return data
    
class CreateCardDevice(CreateView):
    model = Device
    form_class = DeviceForm
    template_name = 'object_card\card_device_form.html'
        
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('card_device', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        data = super(CreateCardDevice, self).get_context_data(**kwargs)
        if self.request.POST:
            data['sim'] = SimFormset(self.request.POST)
        else:
            data['sim'] = SimFormset()
        data['card'] = get_object_or_404(Card, id=self.kwargs['pk'])
        return data

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        phones = context['sim']
        with transaction.atomic(): 
            self.object = form.save(commit=False)
            self.object.enginer_pult = self.request.user
            self.object.changed_pult = datetime.datetime.today()
            self.object = form.save()
            context['card'].device = self.object
            context['card'].status = Card.ACCOUNT
            context['card'].save()
        if phones.is_valid():
            response = super(CreateCardDevice, self).form_valid(form)
            phones.instance = self.object
            phones.save()
            return response
        else:
            return super().form_invalid(form)

class CardPartition(UpdateView):
    model = Device
    form_class = DevicePartForm
    template_name = 'object_card\card_partition_form.html'
        
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('card_partitions', kwargs={'pk': pk})

    def get_object(self, queryset=None):
        card = get_object_or_404(Card, id=self.kwargs['pk'])
        return get_object_or_404(Device, id=card.device.id)

    def get_context_data(self, **kwargs):
        data = super(CardPartition, self).get_context_data(**kwargs)
        if self.request.POST:
            data['partition'] = PartitionFormset(self.request.POST, instance=self.object)
        else:
            data['partition'] = PartitionFormset(instance=self.object)
        data['card'] = get_object_or_404(Card, id=self.kwargs['pk'])
        return data

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        partitions = context['partition']
        with transaction.atomic(): 
            self.object = form.save(commit=False)
            self.object.technican = self.request.user
            self.object.changed_tech = datetime.datetime.today()
            self.object = form.save()
            context['card'].device = self.object
            context['card'].status = Card.MONTAGE
            context['card'].save()
        if partitions.is_valid():
            response = super(CardPartition, self).form_valid(form)
            partitions.instance = self.object
            partitions.save()
            return response
        else:
            return super().form_invalid(form)
