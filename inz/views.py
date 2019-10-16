from django.shortcuts import render
from django.http.response import HttpResponse
from rest_framework import viewsets
from .models import *
from .serializers import *
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
 #   serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
 #   queryset = Group.objects.all()
  #  serializer_class = GroupSerializer

