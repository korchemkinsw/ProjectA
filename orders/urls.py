from django.urls import path

from . import views

urlpatterns = [
    path('', views.orders, name='orders'),
    #path('new_order/', views.NewOrder.as_view(), name='new_order'),
    path('new_order/', views.new_order, name='new_order'),
]
