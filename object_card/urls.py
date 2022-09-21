from django.urls import path

from . import views

urlpatterns = [
    path('devices/', views.ListDevices.as_view(), name='devices'),
    path('add_device/<int:pk>/', views.CreateDevice.as_view(), name='add_device'),
    path('cards/', views.ListCards.as_view(), name='cards'),
]
