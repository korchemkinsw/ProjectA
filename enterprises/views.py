from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView
from django.urls import reverse_lazy

from Project_A import settings

from .models import Enterprise, Position, Staffer
from .forms import AddEnterpriseForm

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

def positions(request):
    latest = Position.objects.all()
    context={
        'my_company': settings.MYCOMPANY,
        'positions': latest,
        'url': 'positions',
        }
    return render(request, "enterprises/positions.html", context)

def staffers(request):
    latest = Staffer.objects.all()
    context={
        'my_company': settings.MYCOMPANY,
        'staffers': latest,
        'url': 'staffers',
        }
    return render(request, "enterprises/staffers.html", context)

class NewEnterprise(CreateView):
    form_class = AddEnterpriseForm
    template_name = 'enterprises/new_enterprise.html'
    success_url = reverse_lazy('enterprises:enterprises')
