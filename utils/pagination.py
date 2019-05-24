from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination
class MyPageNumberPagination(PageNumberPagination):
    # 默认每页显示多少个
    page_size = 3
    page_query_param = 'page'
    # 可以不用默认显示的个数 用size=3 这种方式在请求参数上自定义显示多少个
    page_size_query_param = 'size'
    #  每页最多显示多少个
    max_page_size = 10
    last_page_strings = ('last',)


class MyLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 3
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 10
    template = 'rest_framework/pagination/numbers.html'


class MyCursorPagination(CursorPagination):
    cursor_query_param = 'cursor'
    page_size = 3
    # -id  表示按照id倒序
    ordering = 'id'
    template = 'rest_framework/pagination/previous_and_next.html'
    page_size_query_param = None
    max_page_size = 10
    offset_cutoff = 1000