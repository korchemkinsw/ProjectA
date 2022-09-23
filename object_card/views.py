import datetime
from email.mime import application

from clientele.models import Application
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django_filters.views import FilterView

import object_card

from .forms import CardDeviceFormset, ContractForm, DeviceForm
from .models import Card, Contract, Device, Partition, Zone


class ListDevices(ListView):
    model = Device

    def get_context_data(self, **kwargs):
        data = super(ListDevices, self).get_context_data(**kwargs)
        data['title']='Охранное оборудование'
        data['header']='Охранное оборудование'
        data['tab_head']=(
            'account',
            'клиент',
            'объект',
            'адрес',
        )
        return data

class DetailDevice(DetailView):
    model = Device

    def get_context_data(self, **kwargs):
        data = super(DetailDevice, self).get_context_data(**kwargs)
        device = get_object_or_404(Device, id=self.kwargs['pk'])
        data['title']='Оборудование объекта'
        data['header']=f'Оборудование объекта №{device}' 
        return data

class CreateDevice(CreateView):
    model = Device
    form_class = DeviceForm
    template_name = 'object_card/form.html'
    
    def get_success_url(self):
       pk = self.kwargs['pk']
       return reverse('application', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):

        #if 'control' not in kwargs:
        #    kwargs['control'] = get_object_or_404(Application, id=self.kwargs['pk'])
        data = super(CreateDevice, self).get_context_data(**kwargs)
        '''
        if self.request.POST:
            data['control'] = CardDeviceFormset(self.request.POST)
        else:
            data['control'] = CardDeviceFormset()
        '''
        data['title']='Добавить охранный прибор'
        data['header']=get_object_or_404(Application, id=self.kwargs['pk'])
        return data

        
    def form_valid(self, form):
        application = get_object_or_404(Application, id=self.kwargs['pk'])
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.application = application
            self.object.enginer_pult = self.request.user
            self.object.changed_pult = datetime.datetime.today()
            self.object = form.save()
            application.status = Application.ACCOUNT
            application.save()
        return super(CreateDevice, self).form_valid(form)

class CreateContract(CreateView):
    model = Contract
    form_class = ContractForm
    template_name = 'object_card/form.html'
    
    def get_success_url(self):
       pk = self.kwargs['pk']
       return reverse('application', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        data = super(CreateContract, self).get_context_data(**kwargs)
        data['title']='Назначить реагирование'
        data['header']=get_object_or_404(Application, id=self.kwargs['pk'])
        return data
        
    def form_valid(self, form):
        application = get_object_or_404(Application, id=self.kwargs['pk'])
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.application = application
            self.object.contract_holder = self.request.user
            self.object.changed_ent = datetime.datetime.today()
            self.object = form.save()
            application.status = Application.CONTRACT
            application.save()
        return super(CreateContract, self).form_valid(form)

class ListCards(ListView):
    model = Card

