from rest_framework import permissions
from .models import *


class BelongToLoggedUser(permissions.BasePermission):
    message = 'To nie twoje'

    def has_object_permission(self, request, view, obj):
        temp = Receipt.objects.filter(user=request.user)
        receipt = Receipt.objects.get(pk=obj.receipt)
        if receipt in temp:
            return True


