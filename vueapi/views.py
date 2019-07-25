from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from restapi import models
from utils import seria
from utils.jsonResponse import MyJsonResponse


# Create your views here.

class BlogList(ModelViewSet):
    # 跳过三件套
    authentication_classes = []
    permission_classes = []
    throttle_classes = []
    queryset = models.Blog.objects.all().order_by('-id')
    serializer_class = seria.BolgListSerializers

    def list(self, request, *args, **kwargs):
        # 调用父类的list方法，拿到数据
        data = super(ModelViewSet, self).list(request, *args, **kwargs)
        print(data)
        return MyJsonResponse(data.data, code=1000, msg='ok')


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
                                           auth=params.get('auth'))
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
                                                                            auth=params.get('auth'))
                response = MyJsonResponse(data=[], code=1000, msg='更新成功')
            except Exception as e:
                response = MyJsonResponse(data=[], code=1001, msg=str(e))

        else:
            print(ser.errors)
            response = MyJsonResponse(data=ser.errors, code=-1, msg="fail")
        print(response)
        return response
