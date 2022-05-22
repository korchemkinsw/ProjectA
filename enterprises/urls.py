from django.urls import path
from . import views

urlpatterns = [
    path('', views.enterprises, name='enterprises'),
    path('positions/', views.positions, name='positions'),
    path('staffers/', views.staffers, name='staffers'),
    path('<str:abbreviatedname>', views.enterprise, name='enterprise'),
]
