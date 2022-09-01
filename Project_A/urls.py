from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.i18n import JavaScriptCatalog

from . import views

urlpatterns = [
    path('jsi18n', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    path('enterprises/', include('enterprises.urls')),
    path('orders/', include('orders.urls')),
    path('guide/', views.guide, name='guide'),
    path('clientele/', include('clientele.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
