from django.urls import path

from . import views

urlpatterns = [
    path('devices/', views.ListDevices.as_view(), name='devices'),
    path('add_device/', views.CreateDevice.as_view(), name='add_device'),
    path('cards/', views.ListCards.as_view(), name='cards'),
    path('add_carddev/', views.CreateCardDev.as_view(), name='add_carddev'),
]
