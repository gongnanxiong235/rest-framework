# coding=utf-8

from django.core.paginator import Paginator
from utils.db_cursor import fetchall_to_dict

def paginator(data_list, per_page, page_no):
    """封装Django分页"""
    pages = Paginator(data_list, per_page)

    # 防止超出页数
    if not page_no > 0:
        page_no = 1
    if page_no > pages.num_pages:
        page_no = pages.num_pages

    p = pages.page(page_no)  # 获取本页数据

    data = dict()  # 获取分页信息
    data['count'] = pages.count
    data['page_num'] = pages.num_pages
    data['per_page'] = per_page
    data['current'] = page_no
    data['start_index'] = p.start_index() - 1

    return p.object_list, page_no, data


class QueryWrapper(object):
    """查询集包装器。实现django Paginator需要的必要方法，实现和query一样使用Paginator分页"""

    def __init__(self, sql, params=None, db="default"):
        """
        :param sql: sql语句
        """
        self.sql = sql
        self.params = params
        self.db = db

    def count(self):
        """计算总数据条数"""
        sql = """select count(*) as count from (%s) _count""" % self.sql
        data = fetchall_to_dict(sql)
        if data:
            return data[0]['count'] # 返回总数据条数
        return 0

    def __getitem__(self, k):
        """分页只使用到了切片，此处的k为slice对象"""
        x, y = k.start, k.stop
        sql = self.sql + ' LIMIT {start}, {num}'.format(start=x, num=y - x)
        result = fetchall_to_dict(sql) # 字典列表形式返回
        return result

    def all(self):
        """查询所有数据"""
        return exec_sql(self.sql) # 字典列表形式返回


# def demo_raw():
#     """使用原生sql实现相同分页"""
#     # 示例：查询status=1的用户分页，每页10条，取第2页数据（假设数据量足够）
#     status = 1
#     per_page = 10
#     page_no = 2
#
#     sql = "select id, username, first_name from auth_user where status=%(status)s"
#     params = {"status": status}  # 使用params防止sql注入
#     query = QueryWrapper(sql, params, "default")
#     one_page_data_list, page_no, page_data = paginator(query, per_page, page_no)
#     # one_page_data_list 同ORM获取数据一样
#     print one_page_data_list
#
#
# if __name__ == "__main__":
#     demo_orm()
#     demo_raw()
