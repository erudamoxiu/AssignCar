from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from user import models
from . import serializers
from utils import jsonResponse
from . import checkorder
from user import message_send
import json

# Create your views here.


# 创建派车单
@csrf_exempt
def createAssign(request):
    if request.method == 'POST':
        apply_id = request.POST.get('id').split(',')
        details = request.POST.get('details')
        destfee_id = request.POST.get('destId')
        internalfee_total = request.POST.get('internalFeeTotal')
        marketfee_total = request.POST.get('marketFeeTotal')
        createUser = request.POST.get('createUser')
        departureDate = request.POST.get('departureDate')  # 出发日期
        departureTime = request.POST.get('departureTime')  # 出发时间
        deta = json.loads(details)

        carinfo_list = []
        driver_list = []
        user_list = []
        for item in deta:
            carinfo_list.append(item['carId'])
            driver_list.append(item['driver_id'])
        apply_list = list(apply_id)
        # 产生派车单号
        order_no = checkorder.CheckOrderNo()
        orderNumber = order_no['id__max']
        assign_data = {
            'orderNo': orderNumber,
            'destFeeId': destfee_id,
            'internalFeeTotal': internalfee_total,
            'marketFeeTotal': marketfee_total,
            'createUser': createUser,
            'departureDate': departureDate,
            'departureTime': departureTime,
        }
        try:
            # 产生派车单
            serializer = serializers.AssignSerializer(data=assign_data)
            serializer.is_valid()
            print('ser', serializer.errors)
            serializer.save()
            # 产生的派车单id
            assign_id = serializer.data['id']
        except Exception as e:
            # 保存失败删除对应派车单号
            orderNo = models.UEOrderNumber.objects.get(id=orderNumber)
            orderNo.delete()
            return jsonResponse.error(e)
        detail1_list = []
        detail1_id_list = []  # 所有明细1 id
        detail2_list = []
        detail2_id_list = []  # 所有明细1 id
        try:
            # 遍历明细2保存多个明细2表
            for (item, item1) in zip(driver_list, carinfo_list):
                detail2_data = {
                    'assignId': assign_id,
                    'driverId': item,
                    'carInfoId': item1
                }
                detail2serializer = serializers.Detail2Serializer(data=detail2_data)
                detail2serializer.is_valid()
                detail2serializer.save()
                detail2_id_list.append(detail2serializer.data['id'])
                detail2_list.append(detail2serializer.data)
        except Exception as e:
            models.AssignDetail2.objects.filter(id__in=detail2_id_list).delete()
            models.Assign.objects.filter(id=assign_id).delete()
            return jsonResponse.error(e)

            # 遍历明细1保存多个明细1表
        try:
            for item2 in apply_list:
                detail1_data = {
                    'assignId': assign_id,
                    'applyId': item2
                }
                detail1serializer = serializers.Detail1Serializer(data=detail1_data)
                detail1serializer.is_valid()
                detail1serializer.save()
                detail1_id_list.append(detail1serializer.data['id'])
                detail1_list.append(detail1serializer.data)
        except Exception as e:
            models.AssignDetail1.objects.filter(id__in=detail1_id_list).delete()
            models.Assign.objects.filter(id=assign_id).delete()
            return jsonResponse.error(e)

        # 派车成功发送相关通知
        # 获取各用车单申请人userid
        for i in apply_list:
            userId = models.Apply.objects.get(id=i).serializable_value('userId')
            user_list.append(userId)
        # 获取派车单号
        assign_order_no = models.UEOrderNumber.objects.get(id=orderNumber).serializable_value('orderNo')

        # 获取出发地OK
        departure_id = models.Apply.objects.get(id=apply_list[0]).serializable_value('departureInfoId')
        departure_message = models.DepartureInfo.objects.get(id=departure_id).serializable_value('departure')

        # 获取车型
        carmodel_set = models.CarInfo.objects.filter(id__in=carinfo_list).values('carModelId')
        carModel_list = []
        for i in carmodel_set:
            carmodel = models.CarModel.objects.get(id=i['carModelId']).serializable_value('carModel')
            carModel_list.append(carmodel)
        carModelStr = ",".join(carModel_list)

        # 获取车牌
        licensePlate = models.CarInfo.objects.filter(id__in=carinfo_list).values('licensePlate')
        lic_list = []
        for i in licensePlate:
            lic = i['licensePlate']
            lic_list.append(lic)
        lic_str = ",".join(lic_list)

        # 获取司机名字
        driver = models.Driver.objects.filter(id__in=driver_list).values('driverName__name')
        driver_lis = []
        for i in driver:
            # dri =
            driver_lis.append(i['driverName__name'])
        driver_name = ",".join(driver_lis)

        # 获取手机号码
        phone = models.Driver.objects.filter(id__in=driver_list).values('phone')
        phone_list = []
        for i in phone:
            pho = i['phone']
            phone_list.append(pho)
        phone_str = ",".join(phone_list)
        # 获取目的地OK
        destfee = models.DestFee.objects.get(id=destfee_id).serializable_value('dest')

        # 判断是否有接收到出发日期和时间
        if departureDate is None and departureTime is None:
            departureDate = models.Apply.objects.get(id=apply_list[0]).serializable_value('useDate')
            departureTime = models.Apply.objects.get(id=apply_list[0]).serializable_value('useTime')
        """
        派车成功！请按照出发时间准时前往出发地，谢谢。
        派车单号：
        出发时间：
        出发地：
        车型/车牌：
        司机/手机号：
        目的地：
        """
        message_send.assign_pass_send(user_list, assign_order_no, departureDate, departureTime, departure_message, carModelStr, lic_str, driver_name, phone_str, destfee)
        # 派车成功修改用车单状态为已派车
        for item in apply_list:
            obj = models.Apply.objects.get(id=item)
            obj.approvalStatus = '3'
            obj.save()
        return jsonResponse.success(True)
    return jsonResponse.error('请求方式错误')


# 删除信息
@csrf_exempt
def deleteAssign(request):
    if request.method == 'GET':
        assign_id = request.GET.get('id')
        try:
            as_id = models.Assign.objects.get(id=int(assign_id))
            detail1 = models.AssignDetail1.objects.filter(assignId=as_id)
            detail2 = models.AssignDetail2.objects.filter(assignId=as_id)
        except models.Assign.DoesNotExist:
            return jsonResponse.error('参数错误')
        try:
            detail1.delete()
            detail2.delete()
            as_id.delete()
        except Exception as e:
            return jsonResponse.error(e)
        data = {
            'result': True
        }
        return HttpResponse(data, status=200)


# 查询全部信息
@csrf_exempt
def getAllAssign(request):
    if request.method == 'POST':
        try:
            pageIndex = int(request.POST.get('pageIndex'))
            pageSize = int(request.POST.get('pageSize'))
        except:
            return jsonResponse.error('参数错误')
        startIndex = (pageIndex * pageSize) - pageSize
        endIndex = pageIndex * pageSize
        try:
            total = models.Assign.objects.all().count()
            assign_all = models.Assign.objects.all()[startIndex:endIndex]
        except models.Assign.DoesNotExist:
            return jsonResponse.error('数据不存在')
        try:
            serializer = serializers.AssignSerializer(assign_all, many=True)
            res = serializer.data
            as_list = []
            for item in res:
                as_list.append(item['id'])
            assign_detail1 = models.AssignDetail1.objects.filter(assignId__in=as_list)
            serializer1 = serializers.Detail1Serializer(assign_detail1, many=True)
            return jsonResponse.success({
                "data": serializer.data,
                "total": total,
                'detail1': serializer1.data

            })
        except Exception as e:
            return jsonResponse.error(e)
    return jsonResponse.error('请求方式错误')


# 查询信息
def getAssign(request):
    if request.method == 'GET':
        assign_id = request.GET.get('id')  # 派车单id
        try:
            as_id = models.Assign.objects.get(id=int(assign_id))
            detail1 = models.AssignDetail1.objects.filter(assignId=as_id)
            detail2 = models.AssignDetail2.objects.filter(assignId=as_id)
            serializer = serializers.AssignSerializer(as_id)
            serializer1 = serializers.Detail1Serializer(detail1, many=True)
            serializer2 = serializers.Detail2Serializer(detail2, many=True)
            data = serializer.data
            data = {
                'data': data,
                'detail1': serializer1.data,
                'detail2': serializer2.data
            }
            # return_data = {}
            # for item in data:
            #     return_data[item] = data[item]
            # for item1 in serializer1.data:
            #     return_data[item1] = serializer1.data[item1]
            # for item2 in serializer2.data:
            #     return_data[item2] = serializer2.data[item2]

            return jsonResponse.success(data)
        except models.Assign.DoesNotExist:
            return jsonResponse.error('数据不存在')
    return jsonResponse.error('请求方式错误')

