from django.shortcuts import render

from . import settings


def index(request):
    context={
        'my_company': settings.MYCOMPANY,
        'url': 'index'
        }
    return render(request, "index.html", context)

