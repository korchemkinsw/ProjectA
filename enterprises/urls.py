from django.urls import path
from . import views

urlpatterns = [
    path('', views.enterprises, name='enterprises'),
    path('positions/', views.positions, name='positions'),
    path('staffers/', views.staffers, name='staffers'),
    path('new_enterprise/', views.new_enterprise, name='new_enterprise'),
    path('<str:abbreviatedname>/', views.enterprise, name='enterprise'),
    path('<str:abbreviatedname>/edit/', views.edit_enterprise, name='edit_enterprise'),
]
