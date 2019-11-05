from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import *


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
        res = {'created':'true'}
        return res

    class Meta:
        model = User
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class ReceiptSerializer(serializers.ModelSerializer):
    #to nie dziala
    def create(self,validated_data):
        receipt = Receipt()
        receipt.shop = validated_data['shop']
        try:
            receipt.date = validated_data['date']
        except KeyError:
            receipt.date = None
        request = self.context['request']
        user = None
        if request and request.hasattr('user'):
            user = request.user
        receipt.user = user
        receipt.save()

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
