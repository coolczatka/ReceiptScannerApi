from rest_framework import permissions
from .models import *


class AllowOwner_p(permissions.BasePermission):
    message = 'To nie twoje'

    def has_object_permission(self, request, view, obj):
        temp = Receipt.objects.filter(user=request.user)
        receipt = Receipt.objects.get(pk=obj.receipt)
        if receipt in temp:
            return True

class AllowOwner_r(permissions.BasePermission):
    message = 'To nie twoje'

    def has_object_permission(self, request, view, obj):
        temp = Receipt.objects.filter(user=request.user)
        if obj in temp:
            return True

class UserPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET','POST']:
            return True
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return True if request.user is not None else False
        else:
            return False

