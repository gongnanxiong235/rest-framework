from django.shortcuts import render, HttpResponse
from restapi import models
# from django import views
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import exceptions
from rest_framework.authentication import BasicAuthentication
import time, hashlib
from utils import permission

ORDER_DICT = [{
    'order_id':1,
    'name': 'iphonex max',
    'price': 9888,
    'color': 'red'
}, {
    'order_id':2,
    'name': 'macbook',
    'price': 18000,
    'color': 'white'
}]

def md5(user_name):
    ctime = str(time.time())
    m = hashlib.md5(bytes(user_name, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


# Create your views here.

def create_user(user_type, user_name, password):
    models.UserInfo.objects.create(user_type=user_type, user_name=user_name, password=password)



class AuthView(APIView):

    # 跳过认证
    authentication_classes = []
    # 跳过权限
    permission_classes = []
    # 跳过节流
    throttle_classes = []
    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:

            user_name = request._request.POST.get("user_name")
            password = request._request.POST.get("password")
            obj = models.UserInfo.objects.filter(user_name=user_name, password=password)
            if not obj:
                ret['code'] = 1001
                ret['msg'] = '账户名或者密码错误'
            else:
                # 为用户登录创建token
                token = md5(user_name)
                user_id = obj[0].id
                print('id', user_id)
                # 根据user_id 从token表中查询
                count = models.UserToken.objects.filter(user_id=user_id).count()
                if count == 0:
                    # 创建
                    models.UserToken.objects.create(user_id=user_id, user_token=token)
                else:
                    # 更新
                    models.UserToken.objects.update(user_id=user_id, user_token=token)
                ret['code'] = 1000
                ret['msg'] = 'OK'
                ret['data'] = {'token': token,"user_id":user_id}
        except Exception as e:
            print(e)
            ret['code'] = 1002
            ret['msg'] = '请求异常'

        return JsonResponse(ret)

# 用户认证token校验
class OrderView(APIView):
    # 如果低于个类对象的authenticate方法返回None  交给下一个类对象执行
    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        # request.user request.auth 是固定写法，是Authtication 的authenticate 的返回值（返回值是一个元祖）
        print('user', request.user)
        print('auth', request.auth)
        try:
            ret['data'] = ORDER_DICT
            ret['msg'] = 'OK'
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = '请求异常'
        return JsonResponse(ret)

class UserInfo(APIView):
    # 局部权限
    permission_classes = [permission.SVIPPermission]
    def post(self,request, *args, **kwargs):
        ret = {'code': 1000, 'msg': 'UserInfo'}
        return JsonResponse(ret)