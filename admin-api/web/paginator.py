# -*- coding: utf-8 -*-
"""
@Author ：mengying
@Date   ：2024/6/13 14:27
@Email  : 652044581@qq.com
@Desc   : 分页器
"""
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    # 默认每页显示的数据条数
    page_size = 10

    # 获取URL参数中设置的每页显示数据条数
    page_size_query_param = 'pageSize'

    # 获取URL参数中传入的页码key
    page_query_param = 'pageNum'

    # 最大支持的每页显示的数据条数
    max_page_size = 50

    def paginate_queryset_data(self, queryset, request, view=None, serializer=None):
        try:
            queryset = super().paginate_queryset(queryset, request=request, view=view)
            ser = serializer(queryset, many=True)
            return ser.data
        except NotFound as e:
            return []

    def paginate_queryset_count(self, queryset, request, view=None, serializer=None):
        try:
            res = {}
            queryset = super().paginate_queryset(queryset, request=request, view=view)
            ser = serializer(queryset, many=True)
            res["data"] = ser.data
            res["total"] = self.page.paginator.count
            return res
        except NotFound as e:
            return {}
