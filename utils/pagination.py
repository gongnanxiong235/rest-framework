from rest_framework.pagination import PageNumberPagination
class MyPageNumberPagination(PageNumberPagination):
    # 默认每页显示多少个
    page_size = 3
    page_query_param = 'page'
    # 可以不用默认显示的个数 用size=3 这种方式在请求参数上自定义显示多少个
    page_size_query_param = 'size'
    #  每页最多显示多少个
    max_page_size = 10
    last_page_strings = ('last',)