from django.urls import path
from django.urls import re_path as url

from . import views

urlpatterns = [
    url(r'add_guardobject/(?P<pk>[0-9]+)/(?P<guard>[\w]*)/', views.CreateGuardObject.as_view(), name='add_guardobject'),
    path('guard_object/<int:pk>/', views.DetailGuardObject.as_view(), name='guard_object'),
    path('add_guard_post/<int:pk>/', views.CreateGuardPost.as_view(), name='add_guard_post'),
    url(r'add_employees_post/(?P<pk>[0-9]+)/(?P<selection>[^/]*)', views.AddEmployees.as_view(), name='add_employees_post'),
    url(r'add_employee_post/(?P<pk_post>[0-9]+)/(?P<pk_sec>[0-9]+)/(?P<selection>[^/]*)', views.CreateGuardsOnDuty.as_view(), name='add_employee_post'),
]
