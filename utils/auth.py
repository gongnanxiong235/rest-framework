from rest_framework import exceptions
from restapi import models
from utils.comm_util import check_black_user
from utils.exceptions import BlackException,AuthenticationFailed
# BasicAuthentication  也是继承了BaseAuthentication  可以实现 浏览器认证失败后弹出输入用户名密码的框  需要authenticate_header方法中返回.....
from rest_framework.authentication import BaseAuthentication,BasicAuthentication
class Authtication(BaseAuthentication):
    #  方法名不能变
    def authenticate(self, request):

        '''token校验'''
        if (request._request.GET.get("token") is None):
            token=request._request.POST.get("token")
        else:
            token = request._request.GET.get("token")
            user_id=request.data.get("user_id")
        print('token', token)
        token_obj = models.UserToken.objects.filter(user_token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed("token check failed")
        user_id=token_obj.user_id
        flag=check_black_user(user_id=user_id)
        '''表示在黑名单内'''
        if(flag):
            raise exceptions.AuthenticationFailed("black user")
        # rest_framework内部会把这两个字段赋值给request，用于后续操作
        return (token_obj.user_id, token_obj)

    def authenticate_header(self, request):
        pass


class Authtication1(object):
    #  方法名不能变
    def authenticate(self, request):
        pass

    def authenticate_header(self, request):
        pass