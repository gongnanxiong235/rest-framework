from rest_framework.permissions import BasePermission
from restapi import models


class MyPermission(BasePermission):
    message = 'sorry 您没有权限访问'
    def has_permission(self, request, view):
        user_id = request.user
        user = models.UserInfo.objects.filter(id=user_id).first()
        if (user.user_type == 1 or user.user_type == 2):
            return True
        return False


class SVIPPermission(BasePermission):
    message = 'sorry 您没有权限访问'
    def has_permission(self, request, view):
        user_id = request.user
        user = models.UserInfo.objects.filter(id=user_id).first()
        if (user.user_type == 3):
            return True
        return False
