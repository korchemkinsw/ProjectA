from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from ajax_select import urls as ajax_select_urls
from django.views.i18n import JavaScriptCatalog

from . import views

admin.autodiscover()

urlpatterns = [
    path('jsi18n', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    #path('admin/', admin.site.urls),
    url(r'^ajax_select/', include(ajax_select_urls)),
    url(r'^admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    path('enterprises/', include('enterprises.urls')),
    path('orders/', include('orders.urls')),
    path('guide/', views.guide, name='guide'),
    path('clientele/', include('clientele.urls')),
    path('object_card/', include('object_card.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
