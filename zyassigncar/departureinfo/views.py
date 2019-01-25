import xlrd
from django.db import transaction
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from user import models
from .serializers import *
from utils import jsonResponse


# 添加出发地
@csrf_exempt
def createdateDeparture(request):
    if request.method == 'POST':
        departure = request.POST.get('departure')  # 获取添加数据
        createUser = request.POST.get('createUser')
        try:
            models.DepartureInfo.objects.get(departure=departure)
        # 数据不存在则进行添加
        except models.DepartureInfo.DoesNotExist:
            models.DepartureInfo.objects.create(departure=departure, createUser=createUser)
            return jsonResponse.success(True)
        return jsonResponse.error('数据已存在，请勿重复添加')
    return jsonResponse.error('请求方式错误')


# 修改出发地
@csrf_exempt
def updateDeparture(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        departure = request.POST.get('departure')
        updateUser = request.POST.get('updateUser')
        try:
            departure_id = models.DepartureInfo.objects.get(id=int(id))
        except models.DepartureInfo.DoesNotExist:
            return jsonResponse.error('数据不存在')
        updata_data = {
            'departure': departure,
            'updateUser': updateUser
        }
        serializer = DestDetailSerializer(departure_id, data=updata_data)
        if serializer.is_valid():
            serializer.save()
            return jsonResponse.success(True)
        else:
            return jsonResponse.error(serializer.errors)
    return jsonResponse.error('请求方式错误')

# 删除出发地
@csrf_exempt
def deleteDeparture(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        try:
            departure = models.DepartureInfo.objects.get(id=int(id))
        # 出发地没有数据
        except models.DepartureInfo.DoesNotExist:
            return jsonResponse.error('数据不存在')
        # 出发地数据存在 执行删除语句
        departure.delete()
        return jsonResponse.success(True)
    return jsonResponse.error('请求方式错误')


# 查询全部出发地
@csrf_exempt
def getAllDeparture(request):
    # 查询全部数据
    if request.method == 'POST':
        try:
            pageIndex = int(request.POST.get('pageIndex'))
            pageSize = int(request.POST.get('pageSize'))
        except:
            return jsonResponse.error('参数错误')
        startIndex = (pageIndex * pageSize) - pageSize
        endIndex = pageIndex * pageSize
        try:
            total = models.DepartureInfo.objects.all().count()
            factory_all = models.DepartureInfo.objects.all().order_by('id')[startIndex:endIndex]
        except models.DepartureInfo.DoesNotExist:
            return jsonResponse.error('数据不存在')
        serializer = DestDetailSerializer(factory_all, many=True)
        return jsonResponse.success({
            "data": serializer.data,
            "total": total
        })
    return jsonResponse.error('请求方式错误')


# 查询出发地
def getDeparture(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        try:
            destName = models.DepartureInfo.objects.get(id=int(id))
        except models.DepartureInfo.DoesNotExist:
            return jsonResponse.error('数据不存在')
        serializer = DestDetailSerializer(destName)
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
                        models.DepartureInfo.objects.create(departure=rowValues[0], createUser=createUser)
            except Exception as e:
                return jsonResponse.error(e, {'msg': '出现错误....'})
            return jsonResponse.success({'msg': 'ok'})
        return jsonResponse.error({'msg': '上传文件格式不是xlsx'})
    return jsonResponse.error({'msg': '不是post请求'})


@csrf_exempt
def departure_info(request):
    return render(request, 'departureinfo.html')
