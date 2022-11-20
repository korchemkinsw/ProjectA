from dal import autocomplete
from django.urls import include, path
from django.urls import re_path as url

from . import views

urlpatterns = [
    url(r'^select2/', include('django_select2.urls')),
    url(r'^qteam-autocomplete/$', views.QteamAutocomplete.as_view(), name='qteam-autocomplete'),
    path('cards/', views.FilterCard.as_view(), name='cards'),
    path('card/<int:pk>/', views.DetailCard.as_view(), name='card'),
    path('card_device/<int:pk>/', views.DetailCardDevice.as_view(), name='card_device'),
    path('card_qteam/<int:pk>/', views.DetailCardQteam.as_view(), name='card_qteam'),
    path('card_partitions/<int:pk>/', views.DetailCardPartitions.as_view(), name='card_partitions'),
    path('card_zones/<int:pk>/', views.DetailCardZones.as_view(), name='card_zones'),
    path('card_photos/<int:pk>/', views.DetailCardPhotos.as_view(), name='card_photos'),
    path('add_card_individ/<int:pk>/', views.CreateCardIndividual.as_view(), name='add_card_individ'),
    path('add_card_legal/<int:pk>/', views.CreateCardLegal.as_view(), name='add_card_legal'),
    path('add_card_device/<int:pk>/', views.CreateCardDevice.as_view(), name='add_card_device'),
    path('upd_card_device/<int:pk>/', views.UpdateCardDevice.as_view(), name='upd_card_device'),
    path('add_card_qteam/<int:pk>/', views.CreateQteam.as_view(), name='add_card_qteam'),
    path('del_card_qteam/<int:pk>/', views.delete_qteam, name='del_card_qteam'),
    #path('add_card_qteam/<int:pk>/', views.UpdateCardQteam.as_view(), name='add_card_qteam'),
    #path('add_card_qteam/<int:pk>/add_qteam/', views.CreateQteam.as_view(), name='add_qteam'),
    path('add_card_partition/<int:pk>/', views.CardPartition.as_view(), name='add_card_partition'),
    path('add_card_zone/<int:pk>/', views.CardZone.as_view(), name='add_card_zone'),
    path('upd_card_photos/<int:pk>/', views.UpdateCardPhotos.as_view(), name='upd_card_photos'),
]
