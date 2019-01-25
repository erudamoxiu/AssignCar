import xlrd
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from user import models
from . import serializers
from utils import jsonResponse


# 添加车辆信息
@csrf_exempt
def createdateCarInfo(request):
    if request.method == 'POST':
        add_data = {
            'factoryId': request.POST.get('factoryId'),
            'licensePlate': request.POST.get('licensePlate'),
            'carModelId': request.POST.get('carModelId'),
            'number': request.POST.get('number'),
            'driverId': request.POST.get('driverId'),
            'carFuel': request.POST.get('carFuel'),
            'extraKm': request.POST.get('extraKm'),
            'extraKmPrice': request.POST.get('extraKmPrice'),
            'remark': request.POST.get('remark'),
            'createUser': request.POST.get('createUser')
        }
        serializer = serializers.CarInfoSerializer(data=add_data)
        if serializer.is_valid():
            serializer.save()
            return jsonResponse.success(True)
        else:
            return jsonResponse.error(serializer.errors)
    return jsonResponse.error('请求方式错误')


# 修改车辆信息
@csrf_exempt
def updateCarInfo(request):
    if request.method == 'POST':
        car_id = request.POST.get('id')
        try:
            carinfo_id = models.CarInfo.objects.get(id=int(car_id))
        except models.CarInfo.DoesNotExist:
            return jsonResponse.error('数据不存在')
        # 根据参数对数据库进行数据修改
        updata_data = {
            'factoryId': request.POST.get('factoryId'),
            'licensePlate': request.POST.get('licensePlate'),
            'carModelId': request.POST.get('carModelId'),
            'number': request.POST.get('number'),
            'driverId': request.POST.get('driverId'),
            'carFuel': request.POST.get('carFuel'),
            'extraKm': request.POST.get('extraKm'),
            'extraKmPrice': request.POST.get('extraKmPrice'),
            'remark': request.POST.get('remark'),
            'updateUser': request.POST.get('updateUser'),
        }
        serializer = serializers.CarInfoSerializer(carinfo_id, data=updata_data)
        if serializer.is_valid():
            serializer.save()
            return jsonResponse.success(True)
        else:
            return jsonResponse.error(serializer.errors)
    return jsonResponse.error('请求方式错误')


# 删除车辆信息
@csrf_exempt
def deleteCarInfo(request):
    if request.method == 'GET':
        car_id = request.GET.get('id')
        try:
            id = models.CarInfo.objects.get(id=int(car_id))
        except models.CarInfo.DoesNotExist:
            return jsonResponse.error('数据不存在')
        id.delete()
        return jsonResponse.success(True)
    return jsonResponse.error('请求方式错误')


# 查询全部车辆信息
@csrf_exempt
def getAllCarInfo(request):
    if request.method == 'POST':
        try:
            pageIndex = int(request.POST.get('pageIndex'))
            pageSize = int(request.POST.get('pageSize'))
        except:
            return jsonResponse.error('参数错误')
        startIndex = (pageIndex * pageSize) - pageSize
        endIndex = pageIndex * pageSize
        try:
            total = models.CarInfo.objects.all().count()
            carInfo = models.CarInfo.objects.all().order_by('id')[startIndex:endIndex]
        except models.CarInfo.DoesNotExist:
            return jsonResponse.error('数据不存在')
        serializer = serializers.CarInfoSerializer(carInfo, many=True)
        return jsonResponse.success({
            'data': serializer.data,
            'total': total
        })
    return jsonResponse.error('请求方式错误')


# 查询车辆信息
def getCarInfo(request):
    if request.method == 'GET':
        car_id = request.GET.get('id')
        try:
            id = models.CarInfo.objects.get(id=int(car_id))
        except models.CarInfo.DoesNotExist:
            return jsonResponse.error('数据不存在')
        serializer = serializers.CarInfoSerializer(id)
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
                        factory_id = models.Factory.objects.get(factoryName=rowValues[0])
                        driver_id = models.Driver.objects.get(driverName=rowValues[4])
                        carmodel_id = models.CarModel.objects.get(carModel=rowValues[2])
                        models.CarInfo.objects.create(factoryId=factory_id,
                                                      licensePlate=rowValues[1],
                                                      createUser=createUser,
                                                      carModelId=carmodel_id,
                                                      number=int(rowValues[3]),
                                                      driverId=driver_id,
                                                      carFuel=int(rowValues[5]),
                                                      remark=rowValues[6],
                                                      extraKm=int(rowValues[7]),
                                                      extraKmPrice=int(rowValues[8])),
            except Exception as e:
                return jsonResponse.error(e, {'msg': '出现错误....'})
            return jsonResponse.success({'msg': 'ok'})
        return jsonResponse.error({'msg': '上传文件格式不是xlsx'})
    return jsonResponse.error({'msg': '不是post请求'})


@csrf_exempt
def car_info(request):
    return render(request, 'carinfo.html')