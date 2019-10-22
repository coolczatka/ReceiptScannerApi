from django.shortcuts import render
from django.http.response import HttpResponse
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.decorators import (permission_classes,action)
from rest_framework.permissions import (IsAuthenticated, IsAdminUser, AllowAny)
from .permissions import BelongToLoggedUser

from django.http import HttpResponseForbidden
# Create your views here.

@permission_classes([AllowAny])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@permission_classes([IsAuthenticated])
class ReceiptViewSet(viewsets.ModelViewSet):
    serializer_class = ReceiptSerializer

    def get_queryset(self):
        return Receipt.objects.filter(user=self.request.user)


@permission_classes([BelongToLoggedUser,IsAuthenticated])
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()




