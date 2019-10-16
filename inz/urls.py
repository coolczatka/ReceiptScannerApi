from . import views
from django.urls import path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('costam/',views.hello),
]

if settings.DEBUG:
    urlpatterns += [path(settings.MEDIA_URL+'avatars/<path>',serve,{'document_root':settings.MEDIA_ROOT+'/avatars'})]
    urlpatterns += [path(settings.MEDIA_URL+'receipts/<path>',serve,{'document_root':settings.MEDIA_ROOT+'/receipts'})]
