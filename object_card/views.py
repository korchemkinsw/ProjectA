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

from .forms import DeviceForm
from .models import Card, Contract, Device, Partition, Zone


class ListDevices(ListView):
    model = Device

class CreateDevice(CreateView):
    model = Device
    form_class = DeviceForm
    template_name = 'object_card/form.html'
    success_url = reverse_lazy('devices')

    def get_context_data(self, **kwargs):
        if 'application' not in kwargs:
            kwargs['application'] = get_object_or_404(Application, id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        #context['form'].fields['application'].queryset = Application.objects.filter(id=self.kwargs['pk'])
        context['title']='Добавить охранный прибор'
        context['header']=kwargs['application']
        return context
        
    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.application = get_object_or_404(Application, id=self.kwargs['pk'])
            self.object.enginer_pult = self.request.user
            self.object.changed_pult = datetime.datetime.today()
            self.object = form.save()
        return super(CreateDevice, self).form_valid(form)

class ListCards(ListView):
    model = Card

