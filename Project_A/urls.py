from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.i18n import JavaScriptCatalog

from . import views

admin.autodiscover()

urlpatterns = [
    path('select2/', include('django_select2.urls')),
    path('jsi18n', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    path('enterprises/', include('enterprises.urls')),
    path('orders/', include('orders.urls')),
    path('guide/', views.guide, name='guide'),
    path('clientele/', include('clientele.urls')),
    path('object_card/', include('object_card.urls')),
    path('security_post/', include('security_post.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
