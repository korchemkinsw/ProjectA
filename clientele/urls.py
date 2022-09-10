from django.urls import path

from . import views

urlpatterns = [
    path('legal/', views.ListLegal.as_view(), name='legal'),
    path('individual/', views.ListIndividual.as_view(), name='individual'),
    #path('responsible/', views.ListResponsible.as_view(), name='responsible'),
    path('contactlist/', views.FilterContact.as_view(), name='contactlist'),
    path('contactlist/<int:pk>/',views.DetailContact.as_view(), name='contact'),
    #path('phonebook/', views.CreateContacts.as_view(), name='phonebook'),
    #path('add_phone/', views.CreateContact.as_view(), name='add_phone'),
    #path('add_responsible/', views.CreateResponsible.as_view(), name='add_responsible'),
    path('add_contact/', views.CreateContact.as_view(), name='add_contact'),
]
