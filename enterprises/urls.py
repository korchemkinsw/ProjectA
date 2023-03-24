from django.urls import path
from django.urls import re_path as url

from . import views

urlpatterns = [
    url(r'^worker-autocomplete/$', views.WorkerAutocomplete.as_view(create_field='name',), name='worker-autocomplete'),
    path('weapons/', views.CreateWeapon.as_view() , name='weapons'),
    path('upd_weapon/<int:pk>/', views.UpdateWeapon.as_view() , name='upd_weapon'),
    path('del_weapon/<int:pk>/', views.DeleteWeapon.as_view() , name='del_weapon'),
    path('security/', views.FilterSecurity.as_view() , name='security'),
    path('personalcards/', views.FilterPersonalCard.as_view() , name='personalcards'),
    path('weaponspermits/', views.FilterWeaponsPermit.as_view() , name='weaponspermits'),
    path('security/<int:pk>/', views.DetailSecurity.as_view() , name='det_security'),
    path('add_security/', views.CreateSecurity.as_view() , name='add_security'),
    path('upd_security/<int:pk>/', views.UpdateSecurity.as_view() , name='upd_security'),
    path('add_personalcard/<int:pk>/', views.CreatePersonalCard.as_view() , name='add_personalcard'),
    path('upd_personalcard/<int:pk>/', views.UpdatePersonalCard.as_view() , name='upd_personalcard'),
    path('del_personalcard/<int:pk>/', views.DeletePersonalCard.as_view() , name='del_personalcard'),
    path('add_weaponspermit/<int:pk>/', views.CreateWeaponsPermit.as_view() , name='add_weaponspermit'),
    path('upd_weaponspermit/<int:pk>/', views.UpdateWeaponsPermit.as_view() , name='upd_weaponspermit'),
    path('del_weaponspermit/<int:pk>/', views.DeleteWeaponsPermit.as_view() , name='del_weaponspermit'),
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