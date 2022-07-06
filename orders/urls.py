from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListOrders.as_view(), name='orders'),
    path('create_order/', views.CreateContractorOrder.as_view(), name='new_order'),
    path('update_order/<int:pk>/', views.UpdateContractorOrder.as_view(), name='update_order'),
    path('delete_order/<int:pk>/', views.DeleteOrder.as_view(), name='delete_order'),
    path('<int:pk>',views.DetailOrder.as_view(), name='order'),
    path('add_doc/<int:pk>',views.CreateDocument.as_view(), name='add_doc'),
    path('del_doc/<int:pk>',views.DeleteDocument.as_view(), name='del_doc'),
    path('add_comment/<int:pk>',views.CreateComment.as_view(), name='add_comment'),
    path('filter/', views.order_list, name="filter-list")
]
