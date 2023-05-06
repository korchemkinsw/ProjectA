from django.db import transaction
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, UpdateView)

from enterprises.models import Responseteam

from .forms import BaseGuardPostForm, GuardObjectForm
from .models import GuardObject, GuardPost


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
