from django.urls import path
from django.urls import re_path as url

from . import views

urlpatterns = [
    url(r'add_guardobject/(?P<pk>[0-9]+)/(?P<guard>[\w]*)/', views.CreateGuardObject.as_view(), name='add_guardobject'),
    path('guard_object/<int:pk>/', views.DetailGuardObject.as_view(), name='guard_object'),
    path('add_guard_post/<int:pk>/', views.CreateGuardPost.as_view(), name='add_guard_post'),
]
