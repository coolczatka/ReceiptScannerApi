from django.shortcuts import render
from django.http.response import HttpResponse
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.decorators import (permission_classes,action)
from rest_framework.permissions import (IsAuthenticated, IsAdminUser, AllowAny)
from .permissions import (BelongToLoggedUser,UserPermissions)

from django.http import HttpResponseForbidden
# Create your views here.


@permission_classes([UserPermissions])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@permission_classes([IsAuthenticated])
class ReceiptViewSet(viewsets.ModelViewSet):
    serializer_class = ReceiptSerializer
    queryset = Receipt.objects.all()

    def get_queryset(self):
        return Receipt.objects.filter(user=self.request.user)


@permission_classes([BelongToLoggedUser, IsAuthenticated])
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(receipt=Receipt.objects.get(pk=self.kwargs['id']))

    def create(self, request, *args, **kwargs):
        request.POST['receipt']=self.kwargs['id']
        super().create(request,args,kwargs)

    def partial_update(self, request, *args, **kwargs):
        request.POST['receipt']=self.kwargs['id']
        super().partial_update(request,args,kwargs)


