from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.enterprises, name='enterprises'),
    path('<str:abbreviatedname>', views.enterprise, name='enterprise'),
]
