from rest_framework import serializers
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from .models import *
from .services.ReceiptImageService import ReceiptImageService
import json
import os

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User()
        user.email = validated_data['email']
        try:
            user.first_name = validated_data['first_name']
        except KeyError:
            user.first_name = None
        try:
            user.last_name = validated_data['last_name']
        except KeyError:
            user.last_name = None
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class ReceiptSerializer(serializers.ModelSerializer):

    class Meta:
        model = Receipt
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Picture
        fields = "__all__"
