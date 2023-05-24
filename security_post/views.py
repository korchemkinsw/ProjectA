import re
import urllib
from typing import Any, Optional

from django.db import models, transaction
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, UpdateView)

from enterprises.models import Responseteam, Security
from enterprises.views import FilterSecurity

from .forms import BaseGuardPostForm, GuardObjectForm
from .models import GuardObject, GuardPost, GuardsOnDuty


class DetailGuardObject(DetailView):
    model = GuardObject
    template_name = 'security_post/guard_object.html'

class CreateGuardObject(CreateView):
    model = GuardObject
    form_class = GuardObjectForm
    template_name = 'enterprises/responseteams_filter.html'

    def get(self, request, *args, **kwargs):
        if self.kwargs['guard'] == 'qteam':
            qteam=get_object_or_404(Responseteam, id=self.kwargs['pk'])
            GuardObject(qteam=qteam, number = 1).save()
            return redirect('guard_object', get_object_or_404(GuardObject, qteam=qteam).pk)
        return self.get(request, *args, **kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            if self.kwargs['guard'] == 'qteam':
                self.object.qteam = get_object_or_404(Responseteam, id=self.kwargs['pk'])
                self.object.number = 1
                self.success_url = reverse_lazy('ownresponse')
        self.object = form.save()
        return super(CreateGuardObject, self).form_valid(form)

class CreateGuardPost(CreateView):
    model = GuardPost
    form_class = BaseGuardPostForm
    template_name = 'security_post/guard_object.html'

    def get_context_data(self, **kwargs):
        data = super(CreateGuardPost, self).get_context_data(**kwargs)
        data['action'] = 'create_post'
        data['guardobject'] = get_object_or_404(GuardObject, id=self.kwargs['pk'])
        return data
    
    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.guard_object = get_object_or_404(GuardObject, id=self.kwargs['pk'])
            self.object = form.save()
            self.success_url = reverse('guard_object', args=[str(self.kwargs['pk'])])
        return super(CreateGuardPost, self).form_valid(form)
    
class AddEmployees(FilterSecurity):
    template_name = 'security_post/guard_object.html'

    def get_context_data(self, **kwargs):
        data = super(AddEmployees, self).get_context_data(**kwargs)
        data['action'] = 'add_employees'
        data['selection'] = urllib.parse.unquote(str(self.request.GET.urlencode())) or ''
        data['guardobject'] = get_object_or_404(GuardObject, id=self.kwargs['pk_object'])
        data['post'] = get_object_or_404(GuardPost, id=self.kwargs['pk_post'])
        return data

    def get_queryset(self, **kwargs):
        post = get_object_or_404(GuardPost, id=self.kwargs['pk_post'])
        employees = Security.objects.all()
        for employee in post.personnel.all():
            employees = employees.exclude(id=employee.id)

        if self.kwargs['selection']:
            security =  str(re.search(r'(?<=security=)[а-яА-Я+]*', self.kwargs['selection']).group(0))
            category = str(re.search(r'(?<=category=)[а-яА-Я0-9+]*', self.kwargs['selection']).group(0))
            id_number = str(re.search(r'(?<=id_number=)[а-яА-Я0-9+]*', self.kwargs['selection']).group(0))
            status =  str(re.search(r'(?<=status=)[а-яА-Я+]*', self.kwargs['selection']).group(0))
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
        return employees

class CreateGuardsOnDuty(CreateView):
    model = GuardsOnDuty
    template_name = 'security_post/guard_object.html'

    def get(self, request, *args, **kwargs):
        post=get_object_or_404(GuardPost, id=self.kwargs['pk_post'])
        security=get_object_or_404(Security, id=self.kwargs['pk_sec'])
        GuardsOnDuty(security=security, post = post).save()
        return redirect('add_employees_post', post.guard_object.pk, self.kwargs['pk_post'], self.kwargs['selection'])
    
def dell_employee_post(reqest, pk_object, pk_post, pk_sec):
    employee_post = get_object_or_404(GuardsOnDuty, security=get_object_or_404(Security, id=pk_sec), post=get_object_or_404(GuardPost, id=pk_post))
    employee_post.delete()
    return redirect('add_employees_post', pk_object, pk_post, '')

