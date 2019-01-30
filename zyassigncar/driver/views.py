from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from user import models
from .serializers import *
import xlrd
from django.db import transaction
from utils import jsonResponse
from django.shortcuts import render
# Create your views here.


# 添加司机
@csrf_exempt
def createdateDriver(request):
    if request.method == 'POST':
        name = request.POST.get('driverId')  # 获取添加数据
        phone = request.POST.get('phone')
        factory = request.POST.get('factoryId')
        createUser = request.POST.get('createUser')
        try:
            models.Driver.objects.get(driverName=name)
            # 数据已存在 返回提示
            return jsonResponse.error('司机已存在，请勿重复添加')
        # 数据不存在则进行添加
        except models.Driver.DoesNotExist:
            data = {
                'driverName': name,
                'phone': phone,
                'factoryId': factory,
                'createUser': createUser
            }
            serializer = DriverSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return jsonResponse.success(True)
            else:
                return jsonResponse.error('创建失败')
    return jsonResponse.error('请求方式错误')


# 修改司机
@csrf_exempt
def updateDriver(request):
    if request.method == 'POST':
        driver_id = int(request.POST.get('id'))
        try:
            id = models.Driver.objects.get(id=driver_id)
        except models.Factory.DoesNotExist:
            return jsonResponse.error('数据不存在')
        # 根据参数对数据库进行数据修改
        updata_data = {
            'driverName': request.POST.get('driverName'),
            'phone': request.POST.get('phone'),
            'factoryId': request.POST.get('factoryId'),
            'updateUser': request.POST.get('updateUser')
        }
        serializer = DriverSerializer(id, data=updata_data)
        if serializer.is_valid():
            serializer.save()
            return jsonResponse.success(True)
        else:
            return jsonResponse.error(serializer.errors)
    return jsonResponse.error('请求方式错误')


# 删除司机
@csrf_exempt
def deleteDriver(request):
    if request.method == 'GET':
        driver_id = request.GET.get('id')
        try:
            delete_driver = models.Driver.objects.get(id=driver_id)
        # 司机没有数据
        except models.Driver.DoesNotExist:
            return jsonResponse.error('数据不存在')
        # 司机数据存在 执行删除语句
        delete_driver.delete()
        return jsonResponse.success(True)
    return jsonResponse.error('请求方式错误')


# 查询全部司机
@csrf_exempt
def getAllDriver(request):
    if request.method == 'POST':
        try:
            pageIndex = int(request.POST.get('pageIndex'))
            pageSize = int(request.POST.get('pageSize'))
        except:
            return jsonResponse.error('参数错误')
        startIndex = (pageIndex * pageSize) - pageSize
        endIndex = pageIndex * pageSize
        try:
            total = models.Driver.objects.all().count()
            factory_all = models.Driver.objects.all().order_by('id')[startIndex:endIndex]
        except models.Driver.DoesNotExist:
            return jsonResponse.error('数据不存在')
        serializer = DriverSerializer(factory_all, many=True)
        print('driver_data', serializer.data)
        return jsonResponse.success({
            "data": serializer.data,
            "total": total
        })
    return jsonResponse.error('请求方式错误')


# 查询司机
@csrf_exempt
def getDriver(request):
    if request.method == 'GET':
        driver_id = request.GET.get('id')
        try:
            id = models.Driver.objects.get(id=int(driver_id))
        except models.Driver.DoesNotExist:
            return HttpResponse('False', status=204)
        serializer = DriverSerializer(id)
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
        f = request.FILES['my_file']
        createUser = request.POST.get('createUser')
        type_excel = f.name.split('.')[1]
        if 'xlsx' == type_excel:
            # 开始解析上传的excel表格
            wb = xlrd.open_workbook(filename=None, file_contents=f.read())
            table = wb.sheets()[0]
            nrows = table.nrows  # 行数
            # ncole = table.ncols  # 列数
            try:
                with transaction.atomic():
                    for i in range(1, nrows):
                        rowValues = table.row_values(i)  # 一行的数据
                        factory_id = models.Factory.objects.get(factoryName=rowValues[1])
                        models.Driver.objects.create(driverName=rowValues[0], factoryId=factory_id, createUser=createUser, phone=str(int(rowValues[2])))
            except Exception as e:
                return jsonResponse.error(e, {'msg': '出现错误....'})
            return jsonResponse.success({'msg': 'ok'})
        return jsonResponse.error({'msg': '上传文件格式不是xlsx'})
    return jsonResponse.error({'msg': '不是post请求'})


@csrf_exempt
def driver(request):
    return render(request, 'driver.html')
