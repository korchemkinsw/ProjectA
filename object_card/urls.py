from django.urls import path

from . import views

urlpatterns = [
    path('cards/', views.FilterCard.as_view(), name='cards'),
    path('card/<int:pk>/', views.DetailCard.as_view(), name='card'),
    path('card_device/<int:pk>/', views.DetailCardDevice.as_view(), name='card_device'),
    path('card_qteam/<int:pk>/', views.DetailCardQteam.as_view(), name='card_qteam'),
    path('card_partitions/<int:pk>/', views.DetailCardPartitions.as_view(), name='card_partitions'),
    path('add_card_individ/<int:pk>/', views.CreateCardIndividual.as_view(), name='add_card_individ'),
    path('add_card_legal/<int:pk>/', views.CreateCardLegal.as_view(), name='add_card_legal'),
    path('add_card_device/<int:pk>/', views.CreateCardDevice.as_view(), name='add_card_device'),
    path('add_card_qteam/<int:pk>/', views.UpdateCardQteam.as_view(), name='add_card_qteam'),
    path('add_card_partition/<int:pk>/', views.CardPartition.as_view(), name='add_card_partition'),
    path('add_card_zone/<int:pk>/', views.CreateCardZone.as_view(), name='add_card_zone'),
]
