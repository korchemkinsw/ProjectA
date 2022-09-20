import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django_filters.views import FilterView

from .forms import CardDevForm, DeviceForm
from .models import Card, Contract, Device, Partition, Zone


class ListDevices(ListView):
    model = Device

class CreateDevice(CreateView):
    model = Device
    form_class = DeviceForm
    success_url = reverse_lazy('devices')

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.enginer_pult = self.request.user
            self.object.changed_pult = datetime.datetime.today()
            self.object = form.save()
        return super(CreateDevice, self).form_valid(form)

class ListCards(ListView):
    model = Card

class CreateCardDev(CreateView):
    model = Card
    form_class = CardDevForm
    success_url = reverse_lazy('cards')
