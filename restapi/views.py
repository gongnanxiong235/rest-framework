from django.shortcuts import render, HttpResponse
from restapi import models
# from django import views
# from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import exceptions, serializers
from utils import permission
from utils.jsonResponse import MyJsonResponse
from utils.md import md5, password_md5
from utils.seria import MyField, UserInfoSerializers, UserInfoSerializers2, UserInfoSerializers3, GroupSerializers, \
    RoleSerializers, RoleSer
from utils.pagination import MyPageNumberPagination, MyLimitOffsetPagination, MyCursorPagination
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from utils.db_cursor import fetchall_to_dict, fetchone_to_dict

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


class RegistView(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    def get(self, request, *args, **kwargs):
        user_name = request._request.GET.get('user_name')
        password = request._request.GET.get('password')
        count = models.UserInfo.objects.filter(user_name=user_name).count()
        if (count != 0):
            return MyJsonResponse(data=[], code=1001, msg='用户已经存在')
        models.UserInfo.objects.create(user_name=user_name, password=password_md5(password=password), user_type=1,
                                       group_id=1)
        return MyJsonResponse(data=[], code=1000, msg='ok')


# 跳过所有认证
class AuthView(APIView):
    # 跳过认证
    authentication_classes = []
    # 跳过权限
    permission_classes = []
    # 跳过节流
    throttle_classes = []

    def post(self, request, *args, **kwargs):
        try:
            user_name = request._request.POST.get("user_name")
            password = request._request.POST.get("password")
            print(user_name)
            print(password)
            obj = models.UserInfo.objects.filter(user_name=user_name, password=password_md5(password))
            print(obj)
            if not obj:
                return MyJsonResponse(data=[], code=1001, msg='用户名或密码错误')
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
        except Exception as e:
            print(e)
            return MyJsonResponse(data=[], code=1002, msg='请求异常')
        return MyJsonResponse(data={'token': token, "user_id": user_id}, code=1000, msg='ok')


# 用户认证token校验和黑名单校验
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
            return MyJsonResponse(data=[], code=1002, msg='请求异常')
        return MyJsonResponse(data=ORDER_DICT, code=1000, msg='ok')


# 权限控制
class UserInfo(APIView):
    # 局部权限
    permission_classes = [permission.MyPermission]

    def post(self, request, *args, **kwargs):
        return MyJsonResponse(code=1000, msg='UserInfo', data=ORDER_DICT)


# 版本控制
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


# 解析器
class ParseView(APIView):
    authentication_classes = []
    permission_classes = []
    '''
    如果列表中是JSONParser:表示请求的时候必须以json格式请求 content-type:application/json,
    request._request.POST没数据,如果Header中 content-type:不是application/json 则会报错
    '''

    '''
    request.POST在发JSON数据的时候是取不到值的，只有发urlecoding数据form-data数据才会有值.REST已经对request再次封装了，发送JSON，urlecoding,form-data等常用等常用的数据都封装到data里了，这样就解决了request.POST在发JSON数据`的时候是取不到值的
    '''

    # parser_classes = [JSONParser,FormParser]
    def post(self, request, *args, **kwargs):
        print('post:', request._request.POST)
        print('haha', request._request.POST.get('name', None))
        # request.data 只能返回post请求的数据
        print('data', request.data)
        print('haha', request.data.get('name'))
        return HttpResponse('hello')


class Roleview(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        # 方式一序列化
        # roles=models.UserRole.objects.all().values('id','title')
        # role_list=list(roles)

        '''方式二序列化'''
        roles = models.UserRole.objects.all()
        ser = RoleSerializers(instance=roles, many=True)
        return MyJsonResponse(data=ser.data, code=1000, msg='ok')


# 自定义的的方式序列化
class UseretailView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        # data = json.dumps(UserInfoSerializers2(models.UserInfo.objects.all(), many=True).data, ensure_ascii=False)
        # print(JsonResponse(ret).content)
        # return JsonResponse ( ret ) 被序列化后用HttpResponse  自定义的字典形式用JsonResponse
        # return HttpResponse(data)  HttpResponse 需json.dumps（ser.data）
        '''Response无需json.dumps（ser.data）  直接传ser.data即可 可渲染浏览器'''
        # return Response(UserInfoSerializers2(models.UserInfo.objects.all(), many=True).data)
        #  自定义的方式返回
        return MyJsonResponse(data=UserInfoSerializers2(models.UserInfo.objects.all(), many=True).data, msg='ok',
                              code=1000)


class GroupView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            obj = models.UserGroup.objects.filter(id=pk).first()
            ser = GroupSerializers(instance=obj, many=False)
            return MyJsonResponse(data=ser.data, code=1000, msg='ok')
        except Exception as e:
            print(e)
            return MyJsonResponse(data=[], code=1001, msg='获取组信息失败')


# 以反向生成URL的方式返回
class UserDetailLink(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        obj = models.UserInfo.objects.all()
        # 如果需要反向生成URL  必须加上context={'request': request}
        ser = UserInfoSerializers3(instance=obj, many=True, context={'request': request})
        return MyJsonResponse(ser.data)



# 分页 PageNumberPagination
class PageView(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    def get(self, request, *args, **kwargs):

        # 框架自带的分页
        # http://127.0.0.1:8000/api/v1.0/page1/?page=2这种方式请求
        # pg = PageNumberPagination()
        pg = MyPageNumberPagination()
        # qs = models.UserRole.objects.all()
        qs = models.UserInfo.objects.all()
        pg_queryset = pg.paginate_queryset(queryset=qs, request=request, view=self)
        ser = UserInfoSerializers2(instance=pg_queryset, many=True, )
        # http://127.0.0.1:8000/api/v1.0/page1/?page=1&size=4:显示第一页，每页显示4个
        return MyJsonResponse(data=pg.get_paginated_response(ser.data).data, msg='ok', code=1000)
        # return MyJsonResponse(data=pg.get_paginated_response(UserInfoSerializers2(models.UserInfo.objects.all(), many=True).data).data,msg='ok',code=1000)


# 使用原生sql
class PageViewSql(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    def get(self, request, *args, **kwargs):
        sql = "select user_info.id, user_name,user_type,group_id as `group` from user_info inner join  user_group on user_info.group_id=user_group.id where user_info.group_id=1"
        queryset = fetchall_to_dict(sql=sql)
        print(queryset)
        # 取出所有的group_id
        for row in queryset:
            group_id = row.get("group")
            sql_group = "select id,title from user_group where id=%s"
            query_set_gropu = fetchone_to_dict(sql=sql_group, params=(group_id))
            row["group"] = query_set_gropu
        page_number_pagiration = MyPageNumberPagination()
        page = page_number_pagiration.paginate_queryset(queryset, request=request, view=self)
        result = page_number_pagiration.get_paginated_response(page).data
        return MyJsonResponse(data=result, msg='ok', code=1000)


# 分页 LimitOffsetPagination
class LimitPageView(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    def get(self, request, *args, **kwargs):
        pg = MyLimitOffsetPagination()
        qs = models.UserInfo.objects.all()
        pg_queryset = pg.paginate_queryset(queryset=qs, request=request, view=self)
        ser = UserInfoSerializers2(instance=pg_queryset, many=True, )
        # http://127.0.0.1:8000/api/v1.0/page2/?offset=0&limit=4  从第0个开始取，向后取4条
        return MyJsonResponse(data=pg.get_paginated_response(ser.data).data, msg='ok', code=1000)


# 分页 CursorPagination
class CursorPageView(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    def get(self, request, *args, **kwargs):
        pg = MyCursorPagination()
        qs = models.UserInfo.objects.all()
        pg_queryset = pg.paginate_queryset(queryset=qs, request=request, view=self)
        ser = UserInfoSerializers2(instance=pg_queryset, many=True, )
        # http://127.0.0.1:8000/api/v1.0/page3/?cursor=cD03   页码是加密的 （适合上一页 下一个  不能自己选择页码  增强性能）
        return MyJsonResponse(data=pg.get_paginated_response(ser.data).data, msg='ok', code=1000)


# 视图 GenericAPIView  GenericAPIView继承APIView
class GenericView(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []
    queryset = models.UserInfo.objects.all()
    serializer_class = UserInfoSerializers2
    pagination_class = MyPageNumberPagination

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        pg = self.paginate_queryset(queryset)
        ser = self.get_serializer(instance=pg, many=True)
        return MyJsonResponse(data=ser.data)


# 视图 ModelViewSet re_path(r'^(?P<version>v[0-9].[0-9]+)/model/$', v.ViewsetView.as_view({'get':'list'})),-->发get请求的时候交给list方法处理
# 如果不重写list方法 默认会去找ModelViewSet的list方法-->再去找到ModelViewSet的父类mixins.ListModelMixin中的list方法
class ViewsetView(ModelViewSet):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []
    queryset = models.UserInfo.objects.all()
    serializer_class = UserInfoSerializers2
    pagination_class = MyPageNumberPagination


# 视图重写list方法
class ViewsetView1(ModelViewSet):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []
    queryset = models.UserInfo.objects.all()
    serializer_class = UserInfoSerializers2
    pagination_class = MyPageNumberPagination

    def list(self, request, *args, **kwargs):
        # 调用父类的list方法，拿到数据
        data = super(ModelViewSet, self).list(request, *args, **kwargs)
        print(data)
        return MyJsonResponse(data.data)
