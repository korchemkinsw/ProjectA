from django.urls import path

from . import views

urlpatterns = [
    path('devices/', views.ListDevices.as_view(), name='devices'),
    path('device/<int:pk>/', views.DetailDevice.as_view(), name='device'),
    path('add_device/<int:pk>/', views.CreateDevice.as_view(), name='add_device'),
    path('add_contract/<int:pk>/', views.CreateContract.as_view(), name='add_contract'),
    path('cards/', views.ListCards.as_view(), name='cards'),
]
