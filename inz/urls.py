from . import views
from django.urls import path
from django.conf import settings
from rest_framework.routers import DefaultRouter
from django.views.static import serve
from rest_framework.authtoken import views
from .views import *

router = DefaultRouter()
router.register('users',UserViewSet,base_name='user')
router.register('groups',GroupViewSet,base_name='group')
router.register('receipts',ReceiptViewSet,base_name='receipt')
router.register('products/(?P<id>\d+)',ProductViewSet,base_name='product')
urlpatterns = router.urls

# Auth Token
urlpatterns += [path('login',views.obtain_auth_token)]


if settings.DEBUG:
    urlpatterns += [path(settings.MEDIA_URL+'avatars/<path>',serve,{'document_root':settings.MEDIA_ROOT+'/avatars'})]
    urlpatterns += [path(settings.MEDIA_URL+'receipts/<path>',serve,{'document_root':settings.MEDIA_ROOT+'/receiptss'})]
