from django.shortcuts import render
from Project_A import settings

from .models import Enterprise

def enterprises(request):
    latest = Enterprise.objects.all()[:11]
    context={
        'my_company': settings.MYCOMPANY,
        'enterprises': latest,
        }
    return render(request, "enterprises/enterprises.html", context)
