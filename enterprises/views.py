import csv
import datetime
import re
import urllib

from dal import autocomplete
from dateutil.relativedelta import relativedelta
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages import constants as messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, UpdateView)
from django_filters.views import FilterView

from Project_A.settings import (BIGBOSS, CURRENT, EXPIRATION, EXPIRED,
                                MYCOMPANY, PAGES, SECURITY, WARNING)

from .forms import (AddEnterpriseForm, AddPositionForm, AddStafferForm,
                    ConfirmWorkerForm, PersonalCardForm, PersonalCardsFilter,
                    ResponseteamFilter, ResponseteamForm, SecurityCreateForm,
                    SecurityFilter, SecurityForm, WeaponForm,
                    WeaponsPermitForm, WeaponsPermitsFilter, WorkerForm,
                    WorkersFilter)
from .models import (Enterprise, PersonalCard, Position, Responseteam,
                     Security, Weapon, WeaponsPermit, Worker)


class WorkerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        post = get_object_or_404(Position,post=SECURITY)
        workers = Worker.objects.filter(post=post)
        if not self.request.user.is_authenticated:
            for security in Security.objects.all():
                workers = workers.exclude(id=security.security.id)
            return workers
        for security in Security.objects.all():
                workers = workers.exclude(id=security.security.id)
        qs = workers
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

class FilterResponseteams(FilterView):
    model = Responseteam
    context_object_name = 'responseteams'
    template_name = 'enterprises/responseteams_filter.html'
    filterset_class = ResponseteamFilter

class CreateResponseteam(CreateView):
    model = Responseteam
    form_class = ResponseteamForm
    success_url = reverse_lazy('responseteams')
    template_name = 'enterprises/responseteams_filter.html'

    def get_context_data(self, **kwargs):
        data = super(CreateResponseteam, self).get_context_data(**kwargs)
        data['modal'] = 'createResponseteamModal'
        data['responseteams'] = Responseteam.objects.all()
        return data
    
    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            if form.clean_force() == False:
                self.object.enterprise = None
                self.object = form.save()
        return super(CreateResponseteam, self).form_valid(form)
    
class UpdateResponseteam(UpdateView):
    model = Responseteam
    form_class = ResponseteamForm
    success_url = reverse_lazy('responseteams')
    template_name = 'enterprises/responseteams_filter.html'

    def get_context_data(self, **kwargs):
        qteam = get_object_or_404(Responseteam, id=self.kwargs['pk'])
        data = super(UpdateResponseteam, self).get_context_data(**kwargs)
        data['modal'] = 'updateResponseteamModal'
        data['responseteams'] = Responseteam.objects.all()
        if qteam.enterprise:
            data['form'].fields['force'].initial = True
        return data
    
    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            if form.clean_force() == False:
                self.object.enterprise = None
                self.object = form.save()
        return super(UpdateResponseteam, self).form_valid(form)
    
class DeleteResponseteam(DeleteView):
    model = Responseteam
    success_url = reverse_lazy('responseteams')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class FilterWorkers(FilterView):
    model = Worker
    context_object_name = 'workers'
    template_name = 'enterprises/workers_filter.html'
    filterset_class = WorkersFilter

class EditWorkerView(FormView):
    def dispatch(self, request, *args, **kwargs):
        try:
            if Worker.objects.filter(name__exact = request.POST['name']):      
                self.duplicate = True
            else:
                self.duplicate = False
        except KeyError:
            self.duplicate = False
        return super(EditWorkerView, self).dispatch(request, *args, **kwargs)
    
    def get_form_class(self):
        return ConfirmWorkerForm if self.duplicate else WorkerForm

class CreateWorker(CreateView, EditWorkerView):
    model = Worker
    success_url = reverse_lazy('workers')
    template_name = 'enterprises/worker_form.html'
    
    def get_context_data(self, **kwargs):
        data = super(CreateWorker, self).get_context_data(**kwargs)
        data['action'] = 'create'
        if self.request.POST:
            data['duplicate'] = Worker.objects.filter(name__exact = self.request.POST['name'])
        data['post_security'] = SECURITY
        data['post_bigboss'] = BIGBOSS
        return data
    
    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object = form.save()
            if self.object.post.post == SECURITY:
                self.success_url = reverse('add_security', args=[str(self.object.id)])
        return super(CreateWorker, self).form_valid(form)
    
class UpdateWorker(UpdateView):
    model = Worker
    form_class = WorkerForm
    template_name = 'enterprises/worker_form.html'

    def get_context_data(self, **kwargs):
        data = super(UpdateWorker, self).get_context_data(**kwargs)
        data['action'] = 'update'
        data['post_security'] = SECURITY
        data['post_bigboss'] = BIGBOSS
        data['worker'] = get_object_or_404(Worker, id=self.kwargs['pk'])
        return data

    
class DeleteWorker(DeleteView):
    model = Worker
    success_url = reverse_lazy('workers')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class ListWeapons(ListView):
    model = Weapon
    context_object_name = 'weapon'
    template_name = 'enterprises/weapons.html'

class CreateWeapon(CreateView):
    model = Weapon
    form_class = WeaponForm
    success_url = reverse_lazy('weapons')
    template_name = 'enterprises/weapons.html'

    def get_context_data(self, **kwargs):
        data = super(CreateWeapon, self).get_context_data(**kwargs)
        data['weapons'] = Weapon.objects.all().order_by('release')
        data['modal'] = 'createWeaponModal'
        return data
    
class UpdateWeapon(UpdateView):
    model = Weapon
    form_class = WeaponForm
    success_url = reverse_lazy('weapons')
    template_name = 'enterprises/weapons.html'

    def get_context_data(self, **kwargs):
        data = super(UpdateWeapon, self).get_context_data(**kwargs)
        data['weapons'] = Weapon.objects.all().order_by('release')
        data['modal'] = 'updateWeaponModal'
        return data
    
class DeleteWeapon(DeleteView):
    model = Weapon
    success_url = reverse_lazy('weapons')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class FilterSecurity(FilterView):
    model = Security
    context_object_name = 'security'
    template_name = 'enterprises/security_filter.html'
    filterset_class = SecurityFilter
    #paginate_by = PAGES

    def get_context_data(self, **kwargs):
        data = super(FilterSecurity, self).get_context_data(**kwargs)
        data['expired'] = datetime.datetime.now().date()-relativedelta(years=EXPIRATION, days=1)
        data['warning'] = data['expired']+relativedelta(days=WARNING)
        data['selection'] =  urllib.parse.unquote(str(self.request.GET.urlencode())) or ''
        return data
    
def getfile(request, selection):
    response = HttpResponse(content_type='text/csv') 
    response['Content-Disposition'] = 'attachment; filename="file.csv"'
    employees = Security.objects.all()
    if selection:
        security =  str(re.search(r'(?<=security=)[а-яА-Я+]*', selection).group(0))
        category = str(re.search(r'(?<=category=)[а-яА-Я0-9+]*', selection).group(0))
        id_number = str(re.search(r'(?<=id_number=)[а-яА-Я0-9+]*', selection).group(0))
        status =  str(re.search(r'(?<=status=)[а-яА-Я+]*', selection).group(0))
        security=security.replace('+', ' ')
        category=category.replace('+', ' ')
        id_number=id_number.replace('+', ' ')
        if security:
            employees=employees.filter(security__name__contains=security)
        if category:
            employees=employees.filter(category=category)
        if id_number:
            employees=employees.filter(id_number__contains=id_number)
        if status:
            employees=employees.filter(status=status)
    writer = csv.writer(response) 
    writer.writerow(['Список охранников'])
    writer.writerow(['Фамилия Имя Отчество','Разряд','Номер удостоверения','Статус','Выдано','Продлено'])
    for employee in employees:
        writer.writerow(
            [employee.security.name, employee.category, employee.id_number, employee.status, employee.issue, employee.prolonged]
            ) 
    return response

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

    def dispatch(self, request, *args, **kwargs):
        try:
            if self.kwargs['pk']:      
                self.worker = True
            else:
                self.worker = False
        except KeyError:
            self.worker = False
        return super(CreateSecurity, self).dispatch(request, *args, **kwargs)
    
    def get_form_class(self):
        return SecurityForm if self.worker else SecurityCreateForm

    def get_context_data(self, **kwargs):
        data = super(CreateSecurity, self).get_context_data(**kwargs)
        data['action'] = 'create'
        if self.kwargs['pk']:
            data['worker'] = get_object_or_404(Worker, id=self.kwargs['pk'])
        return data

    def form_valid(self, form):
        form.instance.security_id = self.kwargs['pk']
        with transaction.atomic():
            self.object = form.save(commit=False)
            if self.kwargs['pk']:
                self.object.security = get_object_or_404(Worker, id=self.kwargs['pk'])
            else:
                self.object.security = form.cleaned_data['security']
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
        if self.kwargs['pk']:
            data['worker'] = get_object_or_404(Security, id=self.kwargs['pk']).security
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
    
class FilterPersonalCards(FilterSecurity):
    model = PersonalCard
    context_object_name = 'personalcards'
    template_name = 'enterprises/personalcards_filter.html'
    filterset_class = PersonalCardsFilter

class FilterWeaponsPermits(FilterSecurity):
    model = WeaponsPermit
    context_object_name = 'weaponspermits'
    template_name = 'enterprises/weaponspermits_filter.html'
    filterset_class = WeaponsPermitsFilter

class CreatePersonalCard(CreateView):
    model = PersonalCard
    form_class = PersonalCardForm
    template_name = 'enterprises/security.html'

    def get_success_url(self):
       pk = self.kwargs['pk']
       return reverse('det_security', kwargs={'pk': pk})

    def post(self, request, **kwargs):
        request.POST = request.POST.copy()
        request.POST['security'] = self.kwargs['pk']
        return super(CreatePersonalCard, self).post(request, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(CreatePersonalCard, self).get_context_data(**kwargs)
        data['title'] = 'Персональная карточка '
        data['security'] = get_object_or_404(Security, id=self.kwargs['pk'])
        data['expired'] = datetime.datetime.now().date()-relativedelta(years=EXPIRATION, days=1)
        data['warning'] = data['expired']+relativedelta(days=WARNING)
        data['action'] = 'add_personalcard'
        return data

    def form_valid(self, form):
        form.instance.security_id = self.kwargs['pk']
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.security = get_object_or_404(Security, id=self.kwargs['pk'])
            self.object = form.save()
        return super(CreatePersonalCard, self).form_valid(form)
    
class UpdatePersonalCard(UpdateView):
    model = PersonalCard
    form_class = PersonalCardForm
    template_name = 'enterprises/security.html'

    def get_success_url(self):
       personalcard = get_object_or_404(PersonalCard, id=self.kwargs['pk'])
       pk = personalcard.security.pk
       return reverse('det_security', kwargs={'pk': pk})

    def post(self, request, **kwargs):
        personalcard = get_object_or_404(PersonalCard, id=self.kwargs['pk'])
        request.POST = request.POST.copy()
        request.POST['security'] = personalcard.security.id
        return super(UpdatePersonalCard, self).post(request, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(UpdatePersonalCard, self).get_context_data(**kwargs)
        personalcard = get_object_or_404(PersonalCard, id=self.kwargs['pk'])
        data['title'] = 'Персональная карточка '
        data['security'] = personalcard.security
        data['expired'] = datetime.datetime.now().date()-relativedelta(years=EXPIRATION, days=1)
        data['warning'] = data['expired']+relativedelta(days=WARNING)
        data['action'] = 'upd_personalcard'
        data['id'] = personalcard.pk
        return data

    def form_valid(self, form):
        personalcard = get_object_or_404(PersonalCard, id=self.kwargs['pk'])
        form.instance.security_id = personalcard.security.id
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.security = personalcard.security
            self.object = form.save()
        return super(UpdatePersonalCard, self).form_valid(form)
    
class DeletePersonalCard(DeleteView):
    model = PersonalCard

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        personalcard = get_object_or_404(PersonalCard, id=self.kwargs['pk'],)
        pk = personalcard.security.pk
        return reverse('det_security', kwargs={'pk': pk})

class CreateWeaponsPermit(CreateView):
    model = WeaponsPermit
    form_class = WeaponsPermitForm
    template_name = 'enterprises/security.html'

    def get_success_url(self):
       pk = self.kwargs['pk']
       return reverse('det_security', kwargs={'pk': pk})
    
    def post(self, request, **kwargs):
        request.POST = request.POST.copy()
        request.POST['security'] = self.kwargs['pk']
        return super(CreateWeaponsPermit, self).post(request, **kwargs)
    
    def get_context_data(self, **kwargs):
        data = super(CreateWeaponsPermit, self).get_context_data(**kwargs)
        data['title'] = 'Разрешение на оружие '
        data['security'] = get_object_or_404(Security, id=self.kwargs['pk'])
        data['expired'] = datetime.datetime.now().date()-relativedelta(years=EXPIRATION, days=1)
        data['warning'] = data['expired']+relativedelta(days=WARNING)
        data['action'] = 'add_weaponspermit'
        return data
    
    def form_valid(self, form):
        form.instance.security_id = self.kwargs['pk']
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.security = get_object_or_404(Security, id=self.kwargs['pk'])
            self.object = form.save()
        return super(CreateWeaponsPermit, self).form_valid(form)

class UpdateWeaponsPermit(UpdateView):
    model = WeaponsPermit
    form_class = WeaponsPermitForm
    template_name = 'enterprises/security.html'

    def get_success_url(self):
       weaponspermit = get_object_or_404(WeaponsPermit, id=self.kwargs['pk'])
       pk = weaponspermit.security.pk
       return reverse('det_security', kwargs={'pk': pk})

    def post(self, request, **kwargs):
        weaponspermit = get_object_or_404(WeaponsPermit, id=self.kwargs['pk'])
        request.POST = request.POST.copy()
        request.POST['security'] = weaponspermit.security.id
        return super(UpdateWeaponsPermit, self).post(request, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(UpdateWeaponsPermit, self).get_context_data(**kwargs)
        weaponspermit = get_object_or_404(WeaponsPermit, id=self.kwargs['pk'])
        data['title'] = 'Разрешение на оружие '
        data['security'] = weaponspermit.security
        data['expired'] = datetime.datetime.now().date()-relativedelta(years=EXPIRATION, days=1)
        data['warning'] = data['expired']+relativedelta(days=WARNING)
        data['action'] = 'upd_weaponspermit'
        data['id'] = weaponspermit.pk
        return data

    def form_valid(self, form):
        weaponspermit = get_object_or_404(WeaponsPermit, id=self.kwargs['pk'])
        form.instance.security_id = weaponspermit.security.id
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.security = weaponspermit.security
            self.object = form.save()
        return super(UpdateWeaponsPermit, self).form_valid(form)
    
class DeleteWeaponsPermit(DeleteView):
    model = WeaponsPermit

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        weaponspermit = get_object_or_404(WeaponsPermit, id=self.kwargs['pk'],)
        pk = weaponspermit.security.pk
        return reverse('det_security', kwargs={'pk': pk})

class OwnResponse(FilterResponseteams):
    def get_queryset(self):
        return Responseteam.objects.all().exclude(enterprise=None)
    
    def get_context_data(self, **kwargs):
        data = super(OwnResponse, self).get_context_data(**kwargs)
        data['action'] = 'own'
        data['guard'] = 'qteam'
        return data


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