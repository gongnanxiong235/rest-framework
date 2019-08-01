from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from restapi import models
from utils import seria
from utils.jsonResponse import MyJsonResponse
import datetime, time
from utils.pagination import MyPageNumberPagination


# Create your views here.

class BlogList(ModelViewSet):
    # 跳过三件套
    authentication_classes = []
    permission_classes = []
    throttle_classes = []
    queryset = models.Blog.objects.filter(is_delete=0).order_by('-id')
    serializer_class = seria.BolgListSerializers
    pagination_class = MyPageNumberPagination

    def list(self, request, *args, **kwargs):
        # 调用父类的list方法，拿到数据
        data = super(ModelViewSet, self).list(request, *args, **kwargs)
        print(data.data)
        return MyJsonResponse(data.data, code=1000, msg='ok')


class BlogSeach(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    def post(self, request, *args, **kwargs):
        time.sleep(1)
        serializer_class = seria.BolgListSerializers
        pg = MyPageNumberPagination()
        keyword = request.data.get("keyword", None)
        if keyword is None or keyword == "":
            response = MyJsonResponse(data=[], code=-1, msg="keyword为空")
        else:
            queryset = models.Blog.objects.filter(title__icontains=keyword).order_by('-id')
            pg_queryset = pg.paginate_queryset(queryset=queryset, request=request, view=self)
            ser = serializer_class(instance=pg_queryset, many=True, )
            response = MyJsonResponse(data=pg.get_paginated_response(ser.data).data, msg="ok", code=1000)
        return response


class BlogCreate(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    def get(self, request, *args, **kwargs):
        ser = seria.BolgCreateSerializers(data=request._request.GET)
        # request.query_params==request._resuest.GET
        params = request.query_params
        if ser.is_valid():
            title_count = models.Blog.objects.filter(title=params.get('title')).count()
            if title_count > 0:
                response = MyJsonResponse(data=[], code=1001, msg="title重复")
            else:
                models.Blog.objects.create(title=params.get('title'), url=params.get('url'), date=params.get('date'),
                                           auth=params.get('auth'), create_time=datetime.datetime.now())
                response = MyJsonResponse(data={}, code=1000, msg="success")
        else:
            print(ser.errors)
            response = MyJsonResponse(data=ser.errors, code=-1, msg="fail")
        print(response)
        return response


class BlogUpdate(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    def get(self, request, *args, **kwargs):
        ser = seria.BolgCreateSerializers(data=request._request.GET)
        params = request.query_params
        if ser.is_valid():
            try:
                id = models.Blog.objects.filter(id=params.get("id")).update(title=params.get("title"),
                                                                            date=params.get('date'),
                                                                            auth=params.get('auth'),
                                                                            update_time=datetime.datetime.now())
                response = MyJsonResponse(data=[], code=1000, msg='更新成功')
            except Exception as e:
                response = MyJsonResponse(data=[], code=1001, msg=str(e))

        else:
            print(ser.errors)
            response = MyJsonResponse(data=ser.errors, code=-1, msg="fail")
        print(response)
        return response


class BlogDelete(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    def get(self, request, *args, **kwargs):
        params = request.query_params
        id = params.get("id", None)
        if id is None:
            response = MyJsonResponse(data=[], code=-1, msg="id不能为空")
        else:
            if models.Blog.objects.filter(id=id).count() == 0:
                response = MyJsonResponse(data=[], code=-1, msg="id不存在")
            else:
                models.Blog.objects.filter(id=id).update(is_delete=1)
                response = MyJsonResponse(data=[], code=1000, msg="删除成功")
        return response
