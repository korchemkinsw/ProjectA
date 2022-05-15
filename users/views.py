from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm

class UserCreation(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/new_user.html'
    success_url = reverse_lazy('index')
