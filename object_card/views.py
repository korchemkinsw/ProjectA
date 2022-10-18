import datetime
from msilib.schema import Error

from clientele.models import Contract, Individual, Legal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)
from django_filters.views import FilterView

from .forms import (CardFilter, CardIndividualForm, CardLegalForm,
                    CardPhotoForm, CardQteamForm, DeviceForm, DeviceNoneForm,
                    DeviceUpdateForm, PartitionFormset, SimFormset,
                    ZoneFormset)
from .models import Card, CardPhoto, Device, Partition


class FilterCard(FilterView):
    model = Card
    context_object_name = 'filter'
    template_name = 'object_card/card_filter.html'
    filterset_class = CardFilter
    paginate_by = 15

class DetailCard(DetailView):
    model = Card

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cards']='active'
        return context

class DetailCardDevice(DetailView):
    model = Card
    template_name = 'object_card/card_device_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['device']='active'
        return context

class DetailCardQteam(DetailView):
    model = Card
    template_name = 'object_card/card_qteam_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['qteam']='active'
        return context

class DetailCardPartitions(DetailView):
    model = Card
    template_name = 'object_card/card_partitions_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['partitions']='active'
        return context

class DetailCardZones(DetailView):
    model = Card
    template_name = 'object_card/card_zones_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['zone']='active'
        return context

class DetailCardPhotos(DetailView):
    model = Card
    template_name = 'object_card/card_photos_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos']='active'
        return context

class CreateCardIndividual(CreateView):
    model = Card
    form_class = CardIndividualForm
    template_name = 'form.html'
    success_url = reverse_lazy('individual')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        individ = get_object_or_404(Individual, id=self.kwargs['pk'])
        context['form'].fields['individual'].queryset = Individual.objects.filter(id=self.kwargs['pk']).exclude()
        context['title'] = 'Добавить карточку'
        context['header'] = f'Добавить карточку {individ}'
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
        context = super().get_context_data(**kwargs)
        legal = get_object_or_404(Legal, id=self.kwargs['pk'])
        context['form'].fields['legal'].queryset = Legal.objects.filter(id=self.kwargs['pk']).exclude()
        context['title'] = 'Добавить карточку'
        context['header'] = f'Добавить карточку {legal.fullname}'
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
    template_name = 'object_card/form.html'

    def get_success_url(self):
       pk = self.kwargs['pk']
       return reverse('card_qteam', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        data = super(UpdateCardQteam, self).get_context_data(**kwargs)
        data['card'] = get_object_or_404(Card, id=self.kwargs['pk'])
        if data['card'].legal:
            data['form'].fields['contract'].queryset = Contract.objects.filter(legal=data['card'].legal).exclude()
        else:
            data['form'].fields['contract'].queryset = Contract.objects.filter(individual=data['card'].individual).exclude()
        data['title'] = 'Добавить реагирование'
        data['qteam'] = 'active'
        return data

class CreateCardDevice(CreateView):
    model = Device
    form_class = DeviceForm
    template_name = 'object_card/form.html'
        
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('card_device', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        data = super(CreateCardDevice, self).get_context_data(**kwargs)
        if self.request.POST:
            data['forms'] = SimFormset(self.request.POST, self.request.FILES)
        else:
            data['forms'] = SimFormset()
        data['card'] = get_object_or_404(Card, id=self.kwargs['pk'])
        data['prefix'] ='sim'
        data['title'] = 'Добавить прибор'
        data['button'] = 'Добавить sim'
        data['device'] = 'active'
        return data

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        phones = context['forms']
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

class UpdateCardDevice(UpdateView):
    model = Device
    form_class = DeviceUpdateForm
    template_name = 'object_card/form.html'
        
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('card_device', kwargs={'pk': pk})
    
    def get_object(self, queryset=None):
        card = get_object_or_404(Card, id=self.kwargs['pk'])
        return get_object_or_404(Device, id=card.device.id)
    
    def get_context_data(self, **kwargs):
        data = super(UpdateCardDevice, self).get_context_data(**kwargs)
        if self.request.POST:
            data['forms'] = SimFormset(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['forms'] = SimFormset(instance=self.object)
        data['card'] = get_object_or_404(Card, id=self.kwargs['pk'])
        data['title'] = 'Добавить информацию о приборе'
        data['button'] = 'Добавить sim'
        data['prefix'] = 'sim'
        data['device'] = 'active'
        return data

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        phones = context['forms']
        with transaction.atomic(): 
            self.object = form.save(commit=False)
            self.object.technican = self.request.user
            self.object.changed_tech = datetime.datetime.today()
            self.object = form.save()
            context['card'].device = self.object
            context['card'].status = Card.MONTAGE
            context['card'].save()
            if phones.is_valid():
                response = super(UpdateCardDevice, self).form_valid(form)
                phones.instance = self.object
                phones.save()
                return response
            else:
                return super().form_invalid(form)

class CardPartition(UpdateView):
    model = Device
    form_class = DeviceNoneForm
    template_name = 'object_card/form.html'
        
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('card_partitions', kwargs={'pk': pk})

    def get_object(self, queryset=None):
        card = get_object_or_404(Card, id=self.kwargs['pk'])
        return get_object_or_404(Device, id=card.device.id)

    def get_context_data(self, **kwargs):
        data = super(CardPartition, self).get_context_data(**kwargs)
        if self.request.POST:
            data['forms'] = PartitionFormset(self.request.POST, instance=self.object)
        else:
            data['forms'] = PartitionFormset(instance=self.object)
        data['card'] = get_object_or_404(Card, id=self.kwargs['pk'])
        data['title'] = 'Добавить разделы'
        data['button'] = 'Добавить раздел'
        data['prefix'] = 'partition'
        data['partitions'] = 'active'
        return data

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        partitions = context['forms']
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

class CardZone(UpdateView):
    model = Device
    form_class = DeviceNoneForm
    template_name = 'object_card/form.html'
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('card_zones', kwargs={'pk': pk})

    def get_object(self, queryset=None):
        card = get_object_or_404(Card, id=self.kwargs['pk'])
        return get_object_or_404(Device, id=card.device.id)

    def get_context_data(self, **kwargs):
        data = super(CardZone, self).get_context_data(**kwargs)
        if self.request.POST:
            data['forms'] = ZoneFormset(self.request.POST, instance=self.object)
        else:
            data['forms'] = ZoneFormset(instance=self.object)
        data['card'] = get_object_or_404(Card, id=self.kwargs['pk'])
        data['device'] = get_object_or_404(Device, id=data['card'].device.id)
        for form in data['forms']:
            form.fields['partition'].queryset = Partition.objects.filter(device=data['device'])
        data['title'] = 'Добавить зоны'
        data['button'] = 'Добавить зону'
        data['prefix'] = 'zones'
        data['zone'] = 'active'
        return data

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        zones = context['forms']
        with transaction.atomic(): 
            self.object = form.save(commit=False)
            self.object.technican = self.request.user
            self.object.changed_tech = datetime.datetime.today()
            self.object = form.save()
            context['card'].device = self.object
            context['card'].status = Card.MONTAGE
            context['card'].save()
            if zones.is_valid():
                response = super(CardZone, self).form_valid(form)
                zones.instance = self.object
                zones.save()
                return response
            else:
                return super().form_invalid(form)

