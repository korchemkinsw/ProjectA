import datetime

from dal import autocomplete
from dateutil.relativedelta import relativedelta
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django_filters.views import FilterView

from Project_A.settings import (CURRENT, EXPIRATION, EXPIRED, MYCOMPANY, PAGES,
                                SECURITY, WARNING)

from .forms import (AddEnterpriseForm, AddPositionForm, AddStafferForm,
                    SecurityFilter, SecurityForm)
from .models import Enterprise, Position, Security, Weapon, Worker


class WorkerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        post = get_object_or_404(Position,post=SECURITY)
        if not self.request.user.is_authenticated:
            return Worker.objects.filter(post=post)
        qs = Worker.objects.filter(post=post)
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

class ListWeapons(ListView):
    model = Weapon
    context_object_name = 'weapons'
    template_name = 'enterprises/weapons.html'

class FilterSecurity(FilterView):
    model = Security
    context_object_name = 'security'
    template_name = 'enterprises/security_filter.html'
    filterset_class = SecurityFilter
    paginate_by = PAGES

    def get_context_data(self, **kwargs):
        data = super(FilterSecurity, self).get_context_data(**kwargs)
        data['expired'] = datetime.datetime.now().date()-relativedelta(years=EXPIRATION, days=1)
        data['warning'] = data['expired']+relativedelta(days=WARNING)
        return data

class DetailSecurity(DetailView):
    model = Security
    template_name = 'enterprises/security.html'

    def get_context_data(self, **kwargs):
        data = super(DetailSecurity, self).get_context_data(**kwargs)
        if self.object.prolonged:
            if self.object.prolonged+relativedelta(years=EXPIRATION) < datetime.datetime.now().date():
                self.object.status = EXPIRED
            else:
                self.object.status = CURRENT
        else:
            if self.object.issue+relativedelta(years=EXPIRATION) < datetime.datetime.now().date():
                self.object.status = EXPIRED
            else:
                self.object.status = CURRENT
        self.object.save()
        data['expired'] = datetime.datetime.now().date()-relativedelta(years=EXPIRATION, days=1)
        data['warning'] = data['expired']+relativedelta(days=WARNING)
        return data

class CreateSecurity(CreateView):
    model = Security
    form_class = SecurityForm
    success_url = reverse_lazy('security')

    def get_context_data(self, **kwargs):
        data = super(CreateSecurity, self).get_context_data(**kwargs)
        data['action'] = 'create'
        return data

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            if (self.object.issue or self.object.prolonged) < datetime.datetime.now().date()-relativedelta(years=EXPIRATION):
                self.object.status = EXPIRED
            else:
                self.object.status = CURRENT
            self.object = form.save()
            self.success_url = reverse('det_security', args=[str(self.object.id)])
        return super(CreateSecurity, self).form_valid(form)

class UpdateSecurity(UpdateView):
    model = Security
    form_class = SecurityForm
    
    def get_success_url(self):
       pk = self.kwargs['pk']
       return reverse('det_security', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        data = super(UpdateSecurity, self).get_context_data(**kwargs)
        data['action'] = 'update'
        return data

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            if self.object.prolonged:
                if self.object.prolonged+relativedelta(years=3) < datetime.datetime.now().date():
                    self.object.status = EXPIRED
                else:
                    self.object.status = CURRENT
            else:
                if self.object.issue+relativedelta(years=3) < datetime.datetime.now().date():
                    self.object.status = EXPIRED
                else:
                    self.object.status = CURRENT
            self.object = form.save()
        return super(UpdateSecurity, self).form_valid(form)





def enterprises(request):
    latest = Enterprise.objects.all()
    context={
        'my_company': MYCOMPANY,
        'enterprises': latest,
        'url': 'enterprises',
        }
    return render(request, "enterprises/enterprises.html", context)

def enterprise(request, abbreviatedname):
    enterprise = get_object_or_404(Enterprise,abbreviatedname=abbreviatedname)
    context={
        'my_company': MYCOMPANY,
        'company': enterprise,
        'url': 'card_enterpise',
    }
    return render(request, "enterprises/enterprise.html", context)

def new_enterprise(request):
    form = AddEnterpriseForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(
            request,
            'enterprises/new_enterprise.html',
            {
                'form': form,
                'exp_action': 'new',
                'title_text': 'Новое предприятие',
                'accept': 'Добавить',
                'reject': 'Отменить',
                'to_return': 'enterprises',
                'param': '',
            }
        )
    new_enterprise = form.save(commit=False)
    new_enterprise.save()
    return redirect('enterprises')

def edit_enterprise(request, abbreviatedname):
    enterprise = get_object_or_404(
        Enterprise,
        abbreviatedname=abbreviatedname,
    )
    form = AddEnterpriseForm(
        request.POST or None,
        files=request.FILES or None,
        instance=enterprise,
    )
    if not form.is_valid():
        return render(
            request,
            'enterprises/new_enterprise.html',
            {
                'form': form,
                'exp_action': 'edit',
                'enterprise': enterprise,
                'title_text': 'Редактировать предприятие',
                'accept': 'Изменить',
                'reject': 'Отменить',
                'to_return': 'enterprises',
                'param': abbreviatedname,
            }
        )
    form.save()
    return redirect('enterprise', abbreviatedname)

def del_enterprise(request, abbreviatedname):
    enterprise = get_object_or_404(Enterprise, abbreviatedname=abbreviatedname)
    enterprise.delete()
    return redirect('positions')

def positions(request):
    latest = Position.objects.all()
    context={
        'my_company': MYCOMPANY,
        'positions': latest,
        'url': 'positions',
        }
    return render(request, "enterprises/positions.html", context)

def new_position(request):
    form = AddPositionForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(
            request,
            'enterprises/new_enterprise.html',
            {
                'form': form,
                'exp_action': 'new',
                'title_text': 'Новая должность',
                'accept': 'Добавить',
                'reject': 'Отменить',
                'to_return': 'positions',
                'param': '',
            }
        )
    new_enterprise = form.save(commit=False)
    new_enterprise.save()
    return redirect('positions')

def edit_position(request, id):
    position = get_object_or_404(Position, id=id)
    form = AddPositionForm(
        request.POST or None,
        files=request.FILES or None,
        instance=position,
    )
    if not form.is_valid():
        return render(
            request,
            'enterprises/new_enterprise.html',
            {
                'form': form,
                'exp_action': 'edit',
                'enterprise': position,
                'title_text': 'Редактировать должность',
                'accept': 'Изменить',
                'reject': 'Отменить',
                'to_return': 'positions',
                'param': '',
            }
        )
    form.save()
    return redirect('positions')

def del_position(request, id):
    position = get_object_or_404(Position, id=id)
    position.delete()
    return redirect('positions')

def staffers(request):
    latest = Worker.objects.all()
    context={
        'my_company': MYCOMPANY,
        'staffers': latest,
        'url': 'staffers',
        }
    return render(request, "enterprises/staffers.html", context)

def new_staffer(request):
    form = AddStafferForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(
            request,
            'enterprises/new_enterprise.html',
            {
                'form': form,
                'exp_action': 'new',
                'title_text': 'Новый сотрудник',
                'accept': 'Добавить',
                'reject': 'Отменить',
                'to_return': 'staffers',
                'param': '',
            }
        )
    new_staffer = form.save(commit=False)
    new_staffer.save()
    return redirect('staffers')

def edit_staffer(request, id):
    staffer = get_object_or_404(Worker, id=id)
    form = AddStafferForm(
        request.POST or None,
        files=request.FILES or None,
        instance=staffer,
    )
    if not form.is_valid():
        return render(
            request,
            'enterprises/new_enterprise.html',
            {
                'form': form,
                'exp_action': 'edit',
                'enterprise': staffer,
                'title_text': 'Редактировать сотрудника',
                'accept': 'Изменить',
                'reject': 'Отменить',
                'to_return': 'staffers',
                'param': '',
            }
        )
    form.save()
    return redirect('staffers')

def del_staffer(request, id):
    staffer = get_object_or_404(Position, id=id)
    staffer.delete()
    return redirect('staffers')