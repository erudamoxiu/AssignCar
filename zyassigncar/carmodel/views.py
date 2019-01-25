from django.db import transaction
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from user import models
from .serializers import *
from utils import jsonResponse
import xlrd


# 添加车型
@csrf_exempt
def createdateCarModel(request):
    if request.method == 'POST':
        name = request.POST.get('carModel')  # 获取添加数据
        createUser = request.POST.get('createUser')  # 获取添加数据
        try:
            name = models.CarModel.objects.get(carModel=name)
            return jsonResponse.error('数据不存在')
        except CarModel.DoesNotExist:
            data = {
                'carModel': name,
                'createUser': createUser
            }
            serializer = CarModelDetailSerializer(data=data)
            serializer.is_valid()
            serializer.save()
            return jsonResponse.success(True)
    return jsonResponse.error('请求方式错误')


# 修改车型
@csrf_exempt
def updateCarModel(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        try:
            car_id = models.CarModel.objects.get(id=int(id))
        except models.CarModel.DoesNotExist:
            return jsonResponse.error('数据不存在')
        # 根据参数对数据库进行数据修改
        updata_data = {
            'carModel': request.POST.get('carModel'),
            'updateUser': request.POST.get('updateUser')
        }
        serializer = CarModelDetailSerializer(car_id, data=updata_data)
        if serializer.is_valid():
            serializer.save()
            return jsonResponse.success(True)
        else:
            return jsonResponse.error(serializer.errors)
    return jsonResponse.error('请求方式错误')


# 删除车型
@csrf_exempt
def deleteCarModel(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        try:
            name = models.CarModel.objects.get(id=id)
        except models.CarModel.DoesNotExist:
            return jsonResponse.error('数据不存在')
        name.delete()
        return jsonResponse.success(True)
    return jsonResponse.error('请求方式错误')


# 查询全部车型
@csrf_exempt
def getAllCarModel(request):
    if request.method == 'POST':
        try:
            pageIndex = int(request.POST.get('pageIndex'))
            pageSize = int(request.POST.get('pageSize'))
        except:
            return jsonResponse.error('参数错误')
        startIndex = (pageIndex * pageSize) - pageSize
        endIndex = pageIndex * pageSize
        try:
            total = models.CarModel.objects.all().count()
            carModel_all = models.CarModel.objects.all().order_by('id')[startIndex:endIndex]
        except models.CarModel.DoesNotExist:
            return jsonResponse.error('数据不存在')
        serializer = CarModelDetailSerializer(carModel_all, many=True)
        return jsonResponse.success({
            "data": serializer.data,
            "total": total
        })
    return jsonResponse.error('请求方式错误')


# 查询车型
@csrf_exempt
def getCarModel(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        try:
            carModel_id = models.CarModel.objects.get(id=int(id))
        except models.CarModel.DoesNotExist:
            return jsonResponse.error('数据不存在')
        serializer = CarModelDetailSerializer(carModel_id)
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
            wb = xlrd.open_workbook(filename=None, file_contents=f.read())  # 关键点在于这里
            table = wb.sheets()[0]
            nrows = table.nrows  # 行数
            # ncole = table.ncols  # 列数
            try:
                with transaction.atomic():
                    for i in range(1, nrows):
                        rowValues = table.row_values(i)  # 一行的数据
                        models.CarModel.objects.get_or_create(carModel=rowValues[0], createUser=createUser)
            except Exception as e:
                return jsonResponse.error(e)
            return jsonResponse.success(True)
        return jsonResponse.error('上传文件格式不是xlsx')
    return jsonResponse.error('请求方式错误')


@csrf_exempt
def carmodel(request):
    return render(request, 'carmodel.html')
