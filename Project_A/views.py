from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from . import settings


@login_required
def index(request):
    context={
        'my_company': settings.MYCOMPANY,
        'url': 'index'
        }
    return render(request, "index.html", context)

def guide(request):
    context={
        'my_company': settings.MYCOMPANY,
        'url': 'guide'
        }
    return render(request, "guide.html", context)

def i18n_javascript(request):
  return admin.site.i18n_javascript(request)
