from django.http import HttpResponse, JsonResponse, request
from rest_framework.renderers import JSONRenderer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from user import models

class PagePaginator:

    def __init__(self, table, ser):
        self.table = table
        self.ser = ser

    def paginator(self):
        type1 = models.table.objects.all()
        # 每页三条数据，小于两条则合并到上一页
        paginator = Paginator(type1, 20)
        count = paginator.count

        page = request.GET.get('page', 1)
        currentPage = int(page)

        try:
            customer = paginator.page(currentPage)

        except PageNotAnInteger:
            # 如果用户的页数不是整数时，显示第一页
            customer = paginator.page(1)
        except EmptyPage:
            # 如果用户输入的页数超出范围，显示结果的最后一页
            customer = paginator.page(paginator.num_pages)
        # 序列化需要的字段

        serializer = self.ser(customer.object_list, many=True)

        data = {
            'data': serializer.data,
            'count': count,
        }
        return JSONResponse(data, status=200)


class JSONResponse(HttpResponse):
    """
        向http添加的内容
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)