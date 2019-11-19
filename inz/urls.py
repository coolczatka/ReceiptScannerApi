from . import views
from django.urls import path
from django.conf import settings
from rest_framework.routers import DefaultRouter
from django.views.static import serve
from rest_framework.authtoken import views
from django.conf.urls.static import static
from .views import *

router = DefaultRouter()
router.register('users',UserViewSet,base_name='user')
router.register('groups',GroupViewSet,base_name='group')
router.register('receipts',ReceiptViewSet,base_name='receipt')
router.register('products/(?P<receipt_id>\d+)',ProductViewSet,base_name='product')
router.register('pictures',PictureViewSet,base_name='picture')
urlpatterns = router.urls

# Auth Token
urlpatterns += [path('login',views.obtain_auth_token)]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)