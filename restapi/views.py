from django.shortcuts import render, HttpResponse
from restapi import models
# from django import views
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import exceptions, serializers
from rest_framework.authentication import BasicAuthentication
import time, hashlib, json
from utils import permission
from rest_framework.versioning import URLPathVersioning
from rest_framework.parsers import JSONParser, FormParser

ORDER_DICT = [{
    'order_id': 1,
    'name': 'iphonex max',
    'price': 9888,
    'color': 'red'
}, {
    'order_id': 2,
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
                ret['data'] = {'token': token, "user_id": user_id}
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

    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': 'UserInfo'}
        return JsonResponse(ret)


class Version(APIView):
    # 跳过认证
    authentication_classes = []
    # 跳过权限
    permission_classes = []
    # 跳过节流
    throttle_classes = []

    def get(self, request, *args, **kwargs):
        # 获取版本，如果没有加版本默认为v1  在setting中可以进行默认版本的配置
        print(request.version)
        # 反向获取请求的地址 第一个参数是在urels中配置路由 后面的name  re_path(r'^(?P<version>v[0-9].[0-9]+)/version/$', v.Version.as_view(),name='user'),
        print(request.versioning_scheme.reverse('user', request=request))
        return HttpResponse((request.version, request.versioning_scheme.reverse('user', request=request)))


class ParseView(APIView):
    authentication_classes = []
    permission_classes = []
    '''
    如果列表中是JSONParser:表示请求的时候必须以json格式请求 content-type:application/json,
    request._request.POST没数据,如果Header中 content-type:不是application/json 则会报错
    '''

    # parser_classes = [JSONParser,FormParser]
    def post(self, request, *args, **kwargs):
        print('post:', request._request.POST)
        print('haha', request._request.POST.get('name', None))
        # request.data 只能返回post请求的数据
        print('data', request.data)
        print('haha', request.data.get('name'))
        return HttpResponse('hello')


class RoleSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()


class Roleview(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None, 'data': None}
        '''方式一序列化'''
        # roles=models.UserRole.objects.all().values('id','title')
        # role_list=list(roles)

        '''方式二序列化'''
        roles = models.UserRole.objects.all()
        ser = RoleSerializers(instance=roles, many=True)
        data = json.dumps(ser.data, ensure_ascii=False)  # 显示中文

        ret['data'] = data
        print(ret)
        return JsonResponse(ret)


# 可以对序列化字段的值进行加工和定制  == user_name = serializers.CharField()
class MyField(serializers.CharField):
    def to_representation(self, value):
        if value == 'gongnanxiong':
            return 'shuaige:' + value
        return value


# 序列化 方式1
class UserInfoSerializers(serializers.Serializer):
    user_id = serializers.IntegerField(source='id')
    # user_type=serializers.ChoiceField(choices=((1,'普通用户'),(2,'VIP用户'),(3,'超级VIP 用户')))
    user_type = serializers.SerializerMethodField()
    # user_name = serializers.CharField()
    user_name = MyField()
    group_name = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()

    def get_roles(self, obj):
        role_name = list()
        user_id = obj.id
        role_ids = models.UserinfoRoles.objects.filter(user_id=user_id).values('role_id')
        for rid in role_ids:
            role_obj = models.UserRole.objects.filter(id=rid.get('role_id')).first()
            role_name.append(role_obj.title)
        return role_name

    def get_user_type(self, obj):
        type = obj.user_type
        if type == 1:
            return '普通用户'
        elif type == 2:
            return 'vip用户'
        elif type == 3:
            return ' 超级VIP用户'

    def get_group_name(self, obj):
        print('obj', obj)
        if obj.group_id:
            print(obj.id)
            group = models.UserGroup.objects.filter(id=obj.group_id).first()
            if group:
                return {"id": group.id, 'title': group.title}
        return None


# 序列化 方式2
class UserInfoSerializers2(serializers.ModelSerializer):
    group_name = serializers.SerializerMethodField()
    user_type = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()

    class Meta:
        model = models.UserInfo
        # fields = "__all__"
        fields = ['id', 'user_name', 'user_type', 'group_name', 'roles']
        # depth = 1   有关联关系的自动查询

    def get_roles(self, obj):
        role_name = list()
        user_id = obj.id
        role_ids = models.UserinfoRoles.objects.filter(user_id=user_id).values('role_id')
        for rid in role_ids:
            role_obj = models.UserRole.objects.filter(id=rid.get('role_id')).first()
            role_name.append(role_obj.title)
        return role_name

    def get_user_type(self, obj):
        type = obj.user_type
        if type == 1:
            return '普通用户'
        elif type == 2:
            return 'vip用户'
        elif type == 3:
            return ' 超级VIP用户'

    def get_group_name(self, obj):
        print('obj', obj)
        if obj.group_id:
            print(obj.id)
            group = models.UserGroup.objects.filter(id=obj.group_id).first()
            if group:
                return {"id": group.id, 'title': group.title}
        return None


class UseretailView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        ret = {"code": 1000, "msg": None, "data": None}
        data = json.dumps(UserInfoSerializers(models.UserInfo.objects.all(), many=True).data, ensure_ascii=False)
        ret['data'] = data
        print(JsonResponse(ret).content)
        # return JsonResponse ( ret )
        return HttpResponse(data)


# 序列化 方式3  反向生成url的方式
class UserInfoSerializers3(serializers.ModelSerializer):
    # lookup_field='group_id',lookup_url_kwarg='pk':按照对用的group_id去生成url  如果不写 默认按照userinfo的id来生成
    group = serializers.HyperlinkedIdentityField(view_name='gp', source='group_id', lookup_field='group_id',
                                                 lookup_url_kwarg='pk')

    class Meta:
        model = models.UserInfo
        fields = "__all__"


class GroupSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.UserGroup
        fields = "__all__"


class GroupView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        print('args',args)
        print('kwargs',kwargs)
        print('get',request._request.GET)
        pk = kwargs.get('pk')
        obj = models.UserGroup.objects.filter(id=pk).first()
        ser = GroupSerializers(instance=obj, many=False)
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)


class UserDetailLink(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        obj = models.UserInfo.objects.all()
        # 如果需要反向生成URL  必须加上context={'request': request}
        ser = UserInfoSerializers3(instance=obj, many=True, context={'request': request})
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)
