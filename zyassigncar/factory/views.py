import xlrd
from django.db import transaction
from django.shortcuts import render
from user import models
from .serializers import *
from utils import jsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


# 添加厂别
@csrf_exempt
def createdateFactory(request):
    if request.method == 'POST':
        name = request.POST.get('factoryName')  # 获取添加数据
        createUser = request.POST.get('createUser')
        print('createUser', createUser)
        try:
            name = models.Factory.objects.get(factoryName=name)
            # 数据已存在 返回提示
            return jsonResponse.error
        # 数据不存在则进行添加
        except models.Factory.DoesNotExist:
            data = {
                'factoryName': name,
                'createUser': createUser
            }
            serializer = FactoryDetailSerializer(data=data)
            serializer.is_valid()
            serializer.save()
            return jsonResponse.success(True)
    return jsonResponse.error('请求方式错误')


# 修改厂别
@csrf_exempt
def updateFactory(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        print('id', id)
        try:
            id = models.Factory.objects.get(id=int(id))
        except models.Factory.DoesNotExist:
            return jsonResponse.error('数据不存在')
        # 根据参数对数据库进行数据修改
        updata_data = {
            'factoryName': request.POST.get('factoryName'),
            'updateUser': request.POST.get('updateUser')
        }
        serializer = FactoryDetailSerializer(id, updata_data)
        if serializer.is_valid():
            serializer.save()
            return jsonResponse.success(True)
        else:
            print(serializer.errors)
            return jsonResponse.error
    return jsonResponse.error('请求方式错误')


# 删除厂别
@csrf_exempt
def deleteFactory(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        print('id', id)
        try:
            factory_id = models.Factory.objects.get(id=int(id))
            print("factory_id", factory_id)
        except models.Factory.DoesNotExist:
            return jsonResponse.error('数据不存在')
        factory_id.delete()
        return jsonResponse.success(True)
    return jsonResponse.error('请求方式错误')


# 查询全部厂别
@csrf_exempt
def getAllFactory(request):
    if request.method == 'POST':
        try:
            pageIndex = int(request.POST.get('pageIndex'))
            pageSize = int(request.POST.get('pageSize'))
        except:
            return jsonResponse.error('参数错误')
        startIndex = (pageIndex * pageSize) - pageSize
        endIndex = pageIndex * pageSize
        try:
            total = models.Factory.objects.all().count()
            factory_all = models.Factory.objects.all().order_by('id')[startIndex:endIndex]
        except models.Factory.DoesNotExist:
            return jsonResponse.error('数据不存在')
        serializer = FactoryDetailSerializer(factory_all, many=True)
        return jsonResponse.success({
            'data': serializer.data,
            'total': total
        })
    return jsonResponse.error('请求方式错误')


# 查询厂别
@csrf_exempt
def getFactory(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        try:
            factory_id = models.Factory.objects.get(id=int(id))
        except models.Factory.DoesNotExist:
            return jsonResponse.error('数据不存在')
        serializer = FactoryDetailSerializer(factory_id)
        return jsonResponse.success(serializer.data)
    return jsonResponse.error('请求方式错误')


# 导入资料
@csrf_exempt
def excel_upload(request):
    """
    :param request:
    :return: 上传文件excel表格 ,并进行解析
    """
    if request.method == "POST":
        f = request.FILES['厂别']
        type_excel = f.name.split('.')[1]
        if 'xlsx' == type_excel:
            # 开始解析上传的excel表格
            wb = xlrd.open_workbook(filename=None, file_contents=f.read())  # 关键点在于这里
            table = wb.sheets()[0]
            nrows = table.nrows  # 行数
            # ncole = table.ncols  # 列数
            try:
                with transaction.atomic():
                    for i in range(1, nrows):
                        rowValues = table.row_values(i)  # 一行的数据
                        models.Factory.objects.get_or_create(factoryName=rowValues[0])
            except Exception as e:
                return jsonResponse.error(e, {'msg': '出现错误....'})
            return jsonResponse.success({'msg': 'ok'})
        return jsonResponse.error({'msg': '上传文件格式不是xlsx'})
    return jsonResponse.error({'msg': '不是post请求'})


@csrf_exempt
def factory(request):
    return render(request, 'factory.html')