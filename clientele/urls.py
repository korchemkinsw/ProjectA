from django.urls import path

from . import views

urlpatterns = [
    path('legal/', views.ListLegal.as_view(), name='legal'),
    path('individual/', views.ListIndividual.as_view(), name='individual'),
]
