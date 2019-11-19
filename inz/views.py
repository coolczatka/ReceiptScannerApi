from django.shortcuts import render
from django.http.response import HttpResponse
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import (permission_classes,action)
from rest_framework.permissions import (IsAuthenticated, IsAdminUser, AllowAny)
from .permissions import (AllowOwner_p,AllowOwner_r,UserPermissions)
from .services.ReceiptImageService import ReceiptImageService

from django.http import HttpResponseForbidden
# Create your views here.


@permission_classes([UserPermissions])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@permission_classes([AllowOwner_r, IsAuthenticated])
class ReceiptViewSet(viewsets.ModelViewSet):
    serializer_class = ReceiptSerializer
    queryset = Receipt.objects.all()

    def get_queryset(self):
        return Receipt.objects.filter(user=self.request.user)


@permission_classes([IsAuthenticated])
class PictureViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    queryset = Picture.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()
        name = serializer.data['picture'].split('/')[1]
        path = settings.MEDIA_ROOT+'/'+name
        ris = ReceiptImageService(path)
        ris.findCorners()
        ris.getText()
        data = ris.extractData()
        return Response({'data':data})

@permission_classes([AllowOwner_p, IsAuthenticated])
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(receipt=Receipt.objects.get(pk=self.kwargs['receipt_id']))

    def create(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        receipt = Receipt.objects.get(pk=self.kwargs['receipt_id'])
        serializer.is_valid(raise_exception=True)
        serializer.save(receipt=receipt)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,status=201,headers=headers)




