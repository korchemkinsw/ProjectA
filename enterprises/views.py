from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView
from django.urls import reverse_lazy

from Project_A import settings

from .models import Enterprise, Position, Staffer
from .forms import AddEnterpriseForm, AddPositionForm, AddStafferForm

def enterprises(request):
    latest = Enterprise.objects.all()
    context={
        'my_company': settings.MYCOMPANY,
        'enterprises': latest,
        'url': 'enterprises',
        }
    return render(request, "enterprises/enterprises.html", context)

def enterprise(request, abbreviatedname):
    enterprise = get_object_or_404(Enterprise,abbreviatedname=abbreviatedname)
    context={
        'my_company': settings.MYCOMPANY,
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
        'my_company': settings.MYCOMPANY,
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
    latest = Staffer.objects.all()
    context={
        'my_company': settings.MYCOMPANY,
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
    staffer = get_object_or_404(Staffer, id=id)
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