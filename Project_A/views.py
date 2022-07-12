from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from . import settings

User = get_user_model()

@login_required
def index(request):
    if request.user.role == User.SECRETARY or request.user.role == User.ENGINEER:
        return redirect('/orders/')
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
