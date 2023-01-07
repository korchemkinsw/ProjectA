from django.urls import path
from django.urls import re_path as url

from . import views

urlpatterns = [
    url(r'^qteam-autocomplete/$', views.QteamAutocomplete.as_view(), name='qteam-autocomplete'),
    url(
        r'^person-autocomplete/$',
        views.PersonAutocomplete.as_view(create_field='name',),
        name='person-autocomplete'
    ),
    path('cards/', views.FilterCard.as_view(), name='cards'),
    path('card/<int:pk>/', views.DetailCard.as_view(), name='card'),
    path('card_device/<int:pk>/', views.DetailCardDevice.as_view(), name='card_device'),
    path('card_qteam/<int:pk>/', views.DetailCardQteam.as_view(), name='card_qteam'),
    path('card_partitions/<int:pk>/', views.DetailCardPartitions.as_view(), name='card_partitions'),
    path('card_zones/<int:pk>/', views.DetailCardZones.as_view(), name='card_zones'),
    path('card_responsible/<int:pk>/', views.DetailCardResponsible.as_view(), name='card_responsible'),
    path('card_photos/<int:pk>/', views.DetailCardPhotos.as_view(), name='card_photos'),
    path('add_card_individ/<int:pk>/', views.CreateCardIndividual.as_view(), name='add_card_individ'),
    path('add_card_legal/<int:pk>/', views.CreateCardLegal.as_view(), name='add_card_legal'),
    path('add_card_device/<int:pk>/', views.CreateCardDevice.as_view(), name='add_card_device'),
    path('upd_card_device/<int:pk>/', views.UpdateCardDevice.as_view(), name='upd_card_device'),
    path('upd_card_contract/<int:pk>/', views.UpdateCardContract.as_view(), name='upd_card_contract'),
    path('add_card_gps/<int:pk>/', views.CreateCardGPS.as_view(), name='add_card_gps'),
    path('upd_card_gps/<int:pk>/', views.UpdateCardGPS.as_view(), name='upd_card_gps'),
    path('add_card_qteam/<int:pk>/', views.CreateQteam.as_view(), name='add_card_qteam'),
    path('upd_card_qteam/<int:pk>/', views.UpdateQteam.as_view(), name='upd_card_qteam'),
    path('del_card_qteam/<int:pk>/', views.DeleteQteam.as_view(), name='del_card_qteam'),
    path('upd_card_qnote/<int:pk>/', views.UpdateCardQnote.as_view(), name='upd_card_qnote'),
    path('add_card_partition/<int:pk>/', views.CardPartition.as_view(), name='add_card_partition'),
    path('add_card_zone/<int:pk>/', views.CardZone.as_view(), name='add_card_zone'),
    path('add_card_responsible/<int:pk>/', views.CreateResponsible.as_view(), name='add_card_responsible'),
    path('upd_new_responsible/<int:pk>/', views.UpdateNewResponsible.as_view(), name='upd_new_responsible'),
    path('upd_card_responsible/<int:pk>/', views.UpdateResponsible.as_view(), name='upd_card_responsible'),
    path('del_card_responsible/<int:pk>/', views.DeleteResponsible.as_view(), name='del_card_responsible'),
    path('upd_card_photos/<int:pk>/', views.UpdateCardPhotos.as_view(), name='upd_card_photos'),
]
