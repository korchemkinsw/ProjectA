from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListOrders.as_view(), name='orders'),
    path('create_order/', views.CreateContractorOrder.as_view(), name='new_order'),
    path('update_order/<int:pk>/', views.UpdateContractorOrder.as_view(), name='update_order'),
    path('delete_order/<int:pk>/', views.DeleteOrder.as_view(), name='delete_order'),
]
