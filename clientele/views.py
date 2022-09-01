from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .models import Application, Individual, Legal, Responsible


class ListLegal(ListView):
    model = Legal

class ListIndividual(ListView):
    model = Individual
