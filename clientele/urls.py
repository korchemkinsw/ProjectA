from dal import autocomplete
from django.urls import include, path
from django.urls import re_path as url

from . import views

urlpatterns = [
    url(r'^enterprise-autocomplete/$', views.EnterpriseAutocomplete.as_view(), name='enterprise-autocomplete'),
    path('contactlist/', views.FilterContact.as_view(), name='contactlist'),
    path('add_contact/', views.CreateContact.as_view(), name='add_contact'),
    path('contact/<int:pk>/',views.DetailContact.as_view(), name='contact'),
    path('upd_contact/<int:pk>/',views.UpdateContact.as_view(), name='upd_contact'),
    path('legals/', views.FilterLegal.as_view(), name='legals'),
    path('contracts/', views.FilterContract.as_view(), name='contracts'),
    path('contract/<int:pk>/',views.DetailContract.as_view(), name='contract'),
    path('legal/<int:pk>/',views.DetailLegal.as_view(), name='legal'),
    path('add_contract_legal/<int:pk>/',views.CreateContractLegal.as_view(), name='add_contract_legal'),
    path('upd_contract_legal/<int:pk>/',views.UpdateContractLegal.as_view(), name='upd_contract_legal'),
    path('add_legal/<int:pk>/', views.CreateLegal.as_view(), name='add_legal'),
    path('individual/', views.FilterIndividual.as_view(), name='individual'),
    path('add_individ/<int:pk>/', views.CreateIndividual.as_view(), name='add_individ'),
    path('individual/<int:pk>/',views.DetailIndividual.as_view(), name='individ'),
    path('add_contract_individual/<int:pk>/',views.CreateContractIndividual.as_view(), name='add_contract_individual'),
    path('upd_contract_individual/<int:pk>/',views.UpdateContractIndividual.as_view(), name='upd_contract_individual'),
]
