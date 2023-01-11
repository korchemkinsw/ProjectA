import datetime

from dal import autocomplete
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from clientele.models import Contact, Contract, Individual, Legal
from clientele.views import CreateContact, UpdateContact
from enterprises.models import Responseteam

from .forms import (CardContractForm, CardFilter, CardGPSForm,
                    CardIndividualForm, CardLegalForm, CardQnoteForm,
                    DeviceForm, DeviceNoneForm, DeviceUpdateForm, GPSForm,
                    PartitionFormset, PersonForm, PhotoFormset, QteamForm,
                    SimFormset, ZoneFormset)
from .models import GPS, Card, Device, Partition, Person, Qteam, Zone


class QteamAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Responseteam.objects.none()
        qs = Responseteam.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

class PersonAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Contact.objects.none()
        qs = Contact.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

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

class DetailCardResponsible(DetailView):
    model = Card
    template_name = 'object_card/card_responsible_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['responsible']='active'
        return context

class DetailCardPhotos(DetailView):
    model = Card
    template_name = 'object_card/card_photos_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos']='active'
        return context

class CreateCardIndividual(UserPassesTestMixin, CreateView):
    model = Card
    form_class = CardIndividualForm
    template_name = 'object_card/form_card.html'
    success_url = reverse_lazy('individual')

    def test_func(self):
        if self.request.user.role in ('manager', 'admin'):
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        individ = get_object_or_404(Individual, id=self.kwargs['pk'])
        context['form'].fields['individual'].queryset = Individual.objects.filter(id=self.kwargs['pk']).exclude()
        context['form'].fields['individual'].initial = individ
        context['title'] = 'Добавить карточку'
        context['header'] = f'Добавить карточку {individ}'
        context['action'] = 'add_individual'
        context['cards']='active'
        context['individ'] = individ.pk
        return context

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.status = Card.NEW
            self.object.manager = self.request.user
            self.object.generated = datetime.datetime.today()
            self.object = form.save()
        return super(CreateCardIndividual, self).form_valid(form)

class UpdateCardIndividual(UserPassesTestMixin, UpdateView):
    model = Card
    form_class = CardIndividualForm
    template_name = 'object_card/form_card.html'

    def test_func(self):
        if self.request.user.role in ('manager', 'admin'):
            return True
        return False

    def get_success_url(self):
       pk = self.kwargs['pk']
       return reverse('card', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['individual'].queryset = Individual.objects.filter(id=self.object.individual.pk).exclude()
        context['title'] = 'Добавить карточку'
        context['header'] = f'Добавить карточку {self.object.individual}'
        context['action'] = 'upd_individual'
        context['cards']='active'
        context['individ'] = self.object.individual.pk
        context['account'] = self.object.device.account
        context['transmission'] = self.object.transmission
        context['enterprise'] = self.object.contract.enterprise
        context['contract'] = self.object.contract
        return context

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.status = Card.NEW
            self.object.changed = datetime.datetime.today()
            self.object = form.save()
        return super(UpdateCardIndividual, self).form_valid(form)

class CreateCardLegal(UserPassesTestMixin, CreateView):
    model = Card
    form_class = CardLegalForm
    template_name = 'object_card/form_card.html'#'form.html'
    success_url = reverse_lazy('legals')

    def test_func(self):
        if self.request.user.role in ('manager', 'admin'):
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        legal = get_object_or_404(Legal, id=self.kwargs['pk'])
        context['form'].fields['legal'].queryset = Legal.objects.filter(id=self.kwargs['pk']).exclude()
        context['form'].fields['legal'].initial = legal
        context['title'] = 'Добавить карточку'
        context['header'] = f'Добавить карточку {legal.fullname}'
        context['action'] = 'add_legal'
        context['cards'] = 'active'
        context['legal'] = legal.pk
        return context

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.status = Card.NEW
            self.object.manager = self.request.user
            self.object.generated = datetime.datetime.today()
            self.object = form.save()
        return super(CreateCardLegal, self).form_valid(form)

class UpdateCardLegal(UserPassesTestMixin, UpdateView):
    model = Card
    form_class = CardLegalForm
    template_name = 'object_card/form_card.html'

    def test_func(self):
        if self.request.user.role in ('manager', 'admin'):
            return True
        return False

    def get_success_url(self):
       pk = self.kwargs['pk']
       return reverse('card', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['legal'].queryset = Legal.objects.filter(id=self.object.legal.pk).exclude()
        context['title'] = 'Добавить карточку'
        context['header'] = f'Добавить карточку {self.object.legal.pk}'
        context['action'] = 'upd_legal'
        context['cards']='active'
        context['legal'] = self.object.legal.pk
        context['account'] = self.object.device.account
        context['transmission'] = self.object.transmission
        context['enterprise'] = self.object.contract.enterprise
        context['contract'] = self.object.contract
        return context

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.status = Card.NEW
            self.object.changed = datetime.datetime.today()
            self.object = form.save()
        return super(UpdateCardLegal, self).form_valid(form)

class UpdateCardContract(UserPassesTestMixin, UpdateView):
    model = Card
    form_class = CardContractForm
    template_name = 'object_card/card_qteam_detail.html'

    def test_func(self):
        if self.request.user.role in ('director', 'admin'):
            return True
        return False

    def get_success_url(self):
       pk = self.kwargs['pk']
       return reverse('card_qteam', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        data = super(UpdateCardContract, self).get_context_data(**kwargs)
        data['card'] = get_object_or_404(Card, id=self.kwargs['pk'])
        if data['card'].legal:
            data['form'].fields['contract'].queryset = Contract.objects.filter(legal=data['card'].legal).exclude()
        else:
            data['form'].fields['contract'].queryset = Contract.objects.filter(individual=data['card'].individual).exclude()
        data['qteam'] = 'active'
        data['action'] = 'contract'
        return data

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object = form.save()
            self.object.status = Card.CONTRACT
            if self.object.contract:
                self.object.save()
                return super(UpdateCardContract, self).form_valid(form)
            else:
                return super().form_invalid(form)

class CreateQteam(UserPassesTestMixin, CreateView):
    model = Qteam
    form_class = QteamForm
    template_name = 'object_card/card_qteam_detail.html'
    
    def test_func(self):
        if self.request.user.role in ('director', 'admin'):
            return True
        return False

    def get_success_url(self):
       pk = self.kwargs['pk']
       return reverse('card_qteam', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        data = super(CreateQteam, self).get_context_data(**kwargs)
        data['action'] = 'create'
        data['qteam'] = 'active'
        data['card'] = get_object_or_404(Card, id=self.kwargs['pk'])
        return data

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object = form.save()
            self.object.card = context['card']
            self.object = form.save()
            return super(CreateQteam, self).form_valid(form)

class UpdateQteam(UserPassesTestMixin, UpdateView):
    model = Qteam
    form_class = QteamForm
    template_name = 'object_card/card_qteam_detail.html'
    
    def test_func(self):
        if self.request.user.role in ('director', 'admin'):
            return True
        return False

    def get_success_url(self):
        qteam = get_object_or_404(Qteam, id=self.kwargs['pk'],)
        pk = qteam.card.pk
        return reverse('card_qteam', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        data = super(UpdateQteam, self).get_context_data(**kwargs)
        data['qteam'] = 'active'
        data['card'] = get_object_or_404(Qteam, id=self.kwargs['pk']).card
        return data

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object = form.save()
            self.object.card = context['card']
            self.object = form.save()
            return super(UpdateQteam, self).form_valid(form)

class DeleteQteam(UserPassesTestMixin, DeleteView):
    model = Qteam

    def test_func(self):
        if self.request.user.role in ('director', 'admin'):
            return True
        return False

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        qteam = get_object_or_404(Qteam, id=self.kwargs['pk'],)
        pk = qteam.card.pk
        return reverse('card_qteam', kwargs={'pk': pk})

class UpdateCardQnote(UserPassesTestMixin, UpdateView):
    model = Card
    form_class = CardQnoteForm
    template_name = 'object_card/card_qteam_detail.html'
    
    def test_func(self):
        if self.request.user.role in ('director', 'admin'):
            return True
        return False

    def get_success_url(self):
       pk = self.kwargs['pk']
       return reverse('card_qteam', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        data = super(UpdateCardQnote, self).get_context_data(**kwargs)
        data['card'] = get_object_or_404(Card, id=self.kwargs['pk'])
        data['action'] = 'qnote'
        data['qteam'] = 'active'
        return data

class CreateCardDevice(UserPassesTestMixin, CreateView):
    model = Device
    form_class = DeviceForm
    template_name = 'object_card/form_device.html'

    def test_func(self):
        if self.request.user.role in ('engineer', 'admin'):
            return True
        return False
        
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
        data['action'] = 'add_device'
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

class UpdateCardDevice(UserPassesTestMixin, UpdateView):
    model = Device
    form_class = DeviceForm
    template_name = 'object_card/form_device.html'

    def test_func(self):
        if self.request.user.role in ('engineer', 'technican', 'admin'):
            return True
        return False
        
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
        data['account'] = self.object.account
        data['action'] = 'upd_device'
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
            context['card'].save()
            if phones.is_valid():
                response = super(UpdateCardDevice, self).form_valid(form)
                phones.instance = self.object
                phones.save()
                return response
            else:
                return super().form_invalid(form)

class CardPartition(UserPassesTestMixin, UpdateView):
    model = Device
    form_class = DeviceNoneForm
    template_name = 'object_card/form.html'

    def test_func(self):
        if self.request.user.role in ('engineer', 'technican', 'admin'):
            return True
        return False
        
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

class CardZone(UserPassesTestMixin, UpdateView):
    model = Device
    form_class = DeviceNoneForm
    template_name = 'object_card/form.html'

    def test_func(self):
        if self.request.user.role in ('engineer', 'technican', 'admin'):
            return True
        return False
    
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
        for form in data['forms']:
            queryset = Partition.objects.filter(device=self.object).order_by('number')
            form.fields['partition'].queryset = queryset
            form.fields['partition'].initial = queryset[0]
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

class CreateCardGPS(UserPassesTestMixin, CreateView):
    model = GPS
    form_class = GPSForm
    template_name = 'object_card/card_detail.html'

    def test_func(self):
        if self.request.user.role in ('engineer', 'technican', 'admin'):
            return True
        return False

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('card', kwargs={'pk': pk})
    
    def get_context_data(self, **kwargs):
        data = super(CreateCardGPS, self).get_context_data(**kwargs)
        data['card'] = get_object_or_404(Card, id=self.kwargs['pk'])
        data['cards'] = 'active'
        data['action'] = 'gps_create'
        return data

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        with transaction.atomic(): 
            self.object = form.save(commit=False)
            self.object.card = context['card']
            return super(CreateCardGPS, self).form_valid(form)

class UpdateCardGPS(UserPassesTestMixin, UpdateView):
    model = GPS
    form_class = GPSForm
    template_name = 'object_card/card_detail.html'

    def test_func(self):
        if self.request.user.role in ('engineer', 'technican', 'admin'):
            return True
        return False

    def get_success_url(self):
        card_gps = get_object_or_404(GPS, id=self.kwargs['pk'],)
        pk = card_gps.card.pk
        return reverse('card', kwargs={'pk': pk})
    
    def get_context_data(self, **kwargs):
        data = super(UpdateCardGPS, self).get_context_data(**kwargs)
        data['card'] = get_object_or_404(GPS, id=self.kwargs['pk']).card
        data['cards'] = 'active'
        data['action'] = 'gps_create'
        return data

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        with transaction.atomic(): 
            self.object = form.save(commit=False)
            self.object.card = context['card']
            return super(UpdateCardGPS, self).form_valid(form)

class CreateResponsible(UserPassesTestMixin, CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'object_card/card_responsible_detail.html'
    
    def test_func(self):
        if self.request.user.role in ('manager', 'admin'):
            return True
        return False

    def get_success_url(self):
       pk = self.kwargs['pk']
       return reverse('card_responsible', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        data = super(CreateResponsible, self).get_context_data(**kwargs)
        data['action'] = 'create'
        data['responsible'] = 'active'
        data['card'] = get_object_or_404(Card, id=self.kwargs['pk'])
        if Person.objects.filter(card=data['card']):
            data['form'].fields['number'].initial = Person.objects.filter(card=data['card']).order_by('-number')[0].number + 1
        else:
            data['form'].fields['number'].initial = 1
        return data

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object = form.save()
            self.object.card = context['card']
            self.object = form.save()
            return super(CreateResponsible, self).form_valid(form)

class UpdateNewResponsible(UpdateContact):
    def get_success_url(self):
        person=get_object_or_404(Person, id=self.kwargs['pk'])
        pk = person.card.id
        return reverse('card_responsible', kwargs={'pk': pk})

    def get_object(self, queryset=None):
        person=get_object_or_404(Person, id=self.kwargs['pk'])
        return person.person

class UpdateResponsible(UserPassesTestMixin, UpdateView):
    model = Person
    form_class = PersonForm
    template_name = 'object_card/card_responsible_detail.html'

    def test_func(self):
        if self.request.user.role in ('manager', 'admin'):
            return True
        return False

    def get_success_url(self):
        person=get_object_or_404(Person, id=self.kwargs['pk'])
        pk=person.card.pk
        return reverse('card_responsible', kwargs={'pk': pk})
    
    def get_context_data(self, **kwargs):
        person=get_object_or_404(Person, id=self.kwargs['pk'])
        data = super(UpdateResponsible, self).get_context_data(**kwargs)
        data['id'] = person.id
        data['action'] = 'update'
        data['responsible'] = 'active'
        data['card'] = person.card
        return data

class DeleteResponsible(UserPassesTestMixin, DeleteView):
    model = Person

    def test_func(self):
        if self.request.user.role in ('manager', 'admin'):
            return True
        return False

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        person = get_object_or_404(Person, id=self.kwargs['pk'],)
        pk = person.card.pk
        return reverse('card_responsible', kwargs={'pk': pk})

class UpdateCardPhotos(UserPassesTestMixin, UpdateView):
    model = Card
    form_class = CardGPSForm
    template_name = 'object_card/form.html'

    def test_func(self):
        if self.request.user.role in ('engineer', 'technican', 'admin'):
            return True
        return False

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('card_photos', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        data = super(UpdateCardPhotos, self).get_context_data(**kwargs)
        if self.request.POST:
            data['forms'] = PhotoFormset(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['forms'] = PhotoFormset(instance=self.object)
        data['title'] = 'Добавить фото обьекта'
        data['button'] = 'Добавить фото обьекта'
        data['prefix'] = 'card_photo'
        data['photos'] = 'active'
        return data

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        photos = context['forms']
        with transaction.atomic(): 
            self.object = form.save(commit=False)
            self.object.status = Card.CHANGED
            self.object = form.save()
            if photos.is_valid():
                response = super(UpdateCardPhotos, self).form_valid(form)
                photos.instance = self.object
                photos.save()
                return response
            else:
                return super().form_invalid(form)
