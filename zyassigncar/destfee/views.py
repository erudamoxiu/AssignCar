import xlrd
from django.db import transaction
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from user import models
from .serializers import *
from utils import jsonResponse
# Create your views here.


# 添加目的地与费用
@csrf_exempt
def createdateDestFee(request):
    if request.method == 'POST':
        add_data = {
            'departureInfoId': request.POST.get('departureInfoId'),
            'dest': request.POST.get('dest'),
            'internalFee': request.POST.get('internalFee'),
            'marketFee': request.POST.get('marketFee'),
            'carModelId': request.POST.get('carModelId'),
            'channel': request.POST.get('channel'),
            'otherNote': request.POST.get('otherNote'),
            'createUser': request.POST.get('createUser')
        }
        serializer = DestFeeSerializer(data=add_data)
        if serializer.is_valid():
            serializer.save()
            return jsonResponse.success(True)
        else:
            return jsonResponse.error(serializer.errors)
    return jsonResponse.error('请求方式错误')


# 修改目的地与费用
@csrf_exempt
def updateDestFee(request):
    if request.method == 'POST':
        destfee_Id = request.POST.get('id')
        updata_data = {
            'departureInfoId': request.POST.get('departureInfoId'),
            'dest': request.POST.get('dest'),
            'internalFee': request.POST.get('internalFee'),
            'marketFee': request.POST.get('marketFee'),
            'carModelId': request.POST.get('carModelId'),
            'channel': request.POST.get('channel'),
            'otherNote': request.POST.get('otherNote'),
            'updateUser': request.POST.get('updateUser'),
        }
        print('data', updata_data)
        try:
            dest_id = models.DestFee.objects.get(id=int(destfee_Id))
        except models.DestFee.DoesNotExist:
            return jsonResponse.error('数据不存在')
        serializer = DestFeeSerializer(dest_id, data=updata_data)
        if serializer.is_valid():
            serializer.save()
            print('ser_data', serializer.data)
            return jsonResponse.success(True)
        else:
            print('error', serializer.errors)
            return jsonResponse.error(serializer.errors)
    return jsonResponse.error('请求方式错误')


# 删除目的地与费用
@csrf_exempt
def deleteDestFee(request):

    if request.method == 'GET':
        destId = request.GET.get('id')
        try:
            as_id = models.DestFee.objects.get(id=int(destId))
        except models.DestFee.DoesNotExist:
            return jsonResponse.error('数据不存在')
        as_id.delete()
        return jsonResponse.success(True)
    return jsonResponse.error('请求方式错误')


# 查询全部目的地与费用
@csrf_exempt
def getAllDestFee(request):
    if request.method == 'POST':
        # 查询全部数据
        try:
            pageIndex = int(request.POST.get('pageIndex'))  # 从第几条数据开始
            pageSize = int(request.POST.get('pageSize'))    # 查多少条数据
        except:
            return jsonResponse.error('参数错误')
        startIndex = (pageIndex * pageSize) - pageSize
        endIndex = pageIndex * pageSize
        try:
            total = models.DestFee.objects.filter().count()
            dest_fee_all = models.DestFee.objects.filter().order_by('id')[startIndex:endIndex]
        except models.DestFee.DoesNotExist:
            return jsonResponse.error('数据不存在')
        serializer = DestFeeSerializer(dest_fee_all, many=True)
        return jsonResponse.success({
            "data": serializer.data,
            "total": total
        })
    return jsonResponse.error('请求方式错误')


# 查询目的地与费用
@csrf_exempt
def getDestFee(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        try:
            dest_id = models.DestFee.objects.get(id=int(id))
        except models.DestFee.DoesNotExist:
            return jsonResponse.error('数据不存在')
        serializer = DestFeeSerializer(dest_id)
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
                        departure_id = models.DepartureInfo.objects.get(departure=rowValues[0])
                        carmodel_id = models.CarModel.objects.get(carModel=rowValues[1])
                        models.DestFee.objects.create(departureInfoId=departure_id, carModelId=carmodel_id, dest=rowValues[2], internalFee=str(int(rowValues[3])), marketFee=str(int(rowValues[4])), channel=rowValues[5], otherNote=rowValues[6], createUser=createUser)
            except Exception as e:
                return jsonResponse.error(e, {'msg': '出现错误....'})
            return jsonResponse.success({'msg': 'ok'})
        return jsonResponse.error({'msg': '上传文件格式不是xlsx'})
    return jsonResponse.error({'msg': '不是post请求'})


@csrf_exempt
def dest_fee(request):
    return render(request, 'destfee.html')