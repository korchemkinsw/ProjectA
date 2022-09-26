from django.urls import path

from . import views

urlpatterns = [
    path('cards/', views.FilterCard.as_view(), name='cards'),
    path('card/<int:pk>/', views.DetailCard.as_view(), name='card'),
]
