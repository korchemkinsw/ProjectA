from django.urls import path
from django.urls import re_path as url

from . import views

urlpatterns = [
    url(r'^worker-autocomplete/$', views.WorkerAutocomplete.as_view(create_field='name',), name='worker-autocomplete'),
    path('weapons/', views.ListWeapons.as_view() , name='weapons'),
    path('security/', views.FilterSecurity.as_view() , name='security'),
    path('security/<int:pk>/', views.DetailSecurity.as_view() , name='det_security'),
    path('', views.enterprises, name='enterprises'),
    path('positions/', views.positions, name='positions'),
    path('positions/new/', views.new_position, name='new_position'),
    path('positions/<int:id>/edit/', views.edit_position, name='edit_position'),
    path('positions/<int:id>/delete/', views.del_position, name='del_position'),
    path('staffers/', views.staffers, name='staffers'),
    path('staffers/new/', views.new_staffer, name='new_staffer'),
    path('staffers/<int:id>/edit/', views.edit_staffer, name='edit_staffer'),
    path('staffers/<int:id>/delete/', views.del_staffer, name='del_staffer'),
    path('new_enterprise/', views.new_enterprise, name='new_enterprise'),
    path('<str:abbreviatedname>/', views.enterprise, name='enterprise'),
    path('<str:abbreviatedname>/edit/', views.edit_enterprise, name='edit_enterprise'),
    path('<str:abbreviatedname>/delete/', views.del_enterprise, name='del_enterprise'),
]