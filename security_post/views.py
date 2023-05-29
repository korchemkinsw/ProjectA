import re
import urllib
from typing import Any, Optional

from django.db import models, transaction
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, UpdateView)
from django_filters.views import FilterView

from clientele.models import Contract
from enterprises.models import Responseteam, Security
from enterprises.views import FilterSecurity

from .forms import BaseGuardPostForm, GuardObjectFilter, GuardObjectForm
from .models import GuardObject, GuardPost, GuardsOnDuty


class FilterGuardObjects(FilterView):
    model = GuardObject
    context_object_name = 'guardobjects'
    template_name = 'security_post/guard_objects_filter.html'
    filterset_class = GuardObjectFilter

    def get_queryset(self, **kwargs):
        return GuardObject.objects.all().exclude(contract=None)



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
            GuardObject(qteam=qteam, number = 0).save()
            return redirect('guard_object', get_object_or_404(GuardObject, qteam=qteam).pk)
        if self.kwargs['guard'] == 'contract':
            contract=get_object_or_404(Contract, id=self.kwargs['pk'])
            GuardObject(contract=contract, number = 0).save()
            return redirect('guard_object', get_object_or_404(GuardObject, contract=contract).pk)
        return self.get(request, *args, **kwargs)

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
        guard_object = get_object_or_404(GuardObject, id=self.kwargs['pk'])
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.guard_object = guard_object
            self.object = form.save()
            guard_object.number = guard_object.number + 1
            guard_object.save()
            self.success_url = reverse('guard_object', args=[str(self.kwargs['pk'])])
        return super(CreateGuardPost, self).form_valid(form)
    
class AddEmployees(FilterSecurity):
    template_name = 'security_post/guard_object.html'

    def get_context_data(self, **kwargs):
        data = super(AddEmployees, self).get_context_data(**kwargs)
        data['action'] = 'add_employees'
        data['selection'] = urllib.parse.unquote(str(self.request.GET.urlencode())) or ''
        data['guardobject'] = get_object_or_404(GuardObject, id=self.kwargs['pk_object'])
        data['post_number'] = get_object_or_404(GuardPost, id=self.kwargs['pk_post'])
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

