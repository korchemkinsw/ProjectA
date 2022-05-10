from django.shortcuts import get_object_or_404, render
from Project_A import settings

from .models import Enterprise

def enterprises(request):
    latest = Enterprise.objects.all()[:11]
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
