from django.urls import path

from . import views

urlpatterns = [
    path('contactlist/', views.FilterContact.as_view(), name='contactlist'),
    path('contactlist/<int:pk>/',views.DetailContact.as_view(), name='contact'),
    path('add_contact/', views.CreateContact.as_view(), name='add_contact'),
    path('legals/', views.ListLegal.as_view(), name='legals'),
    path('legals/<int:pk>/',views.DetailLegal.as_view(), name='legal'),
    path('add_legal/<int:pk>/', views.CreateLegal.as_view(), name='add_legal'),
    path('individual/', views.ListIndividual.as_view(), name='individual'),
    path('add_individ/<int:pk>/', views.CreateIndividual.as_view(), name='add_individ'),
    path('individual/<int:pk>/',views.DetailIndividual.as_view(), name='individ'),
    #path('responsible/', views.ListResponsible.as_view(), name='responsible'),
    #path('phonebook/', views.CreateContacts.as_view(), name='phonebook'),
    #path('add_phone/', views.CreateContact.as_view(), name='add_phone'),
    #path('add_responsible/', views.CreateResponsible.as_view(), name='add_responsible'),
    
]
