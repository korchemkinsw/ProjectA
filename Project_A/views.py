from django.shortcuts import render
from . import settings

def index(request):
    context={'my_company': settings.MYCOMPANY}
    return render(request, "index.html", context)