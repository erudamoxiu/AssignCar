import datetime
from user import models
from utils import jsonResponse
from . import serializers
from django.db.models import Max


def CheckOrderNo():
    oreder_date = datetime.datetime.now().strftime("%Y%m%d")
    ord_No = '0001'
    try:
        orderNo = models.UEOrderNumber.objects.all().aggregate(Max('id'))
        # 通过最大值找到对应数据
        orde_no = models.UEOrderNumber.objects.get(id=orderNo['id__max'])
        # 最大订单号实例化
        order_NO = orde_no.orderNo
        # 取出时间进行类型转换
        orderNo_datetime = orde_no.createDate.strftime("%Y%m%d")

        # 判断当前时间是否大于创建时间
        if int(oreder_date) > int(orderNo_datetime):
            # 重置订单号
            orderNumber = 'UE'+oreder_date + ord_No
            data = {
                'orderNo': orderNumber
            }
            serializer = serializers.UeOrderNumberSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                orderNumber = models.UEOrderNumber.objects.all().aggregate(Max('id'))
                return orderNumber
            else:
                data = {
                    'result': False,
                }
                return jsonResponse.error(data)
        else:
            # 如果是当天创建则找到最大订单号+1
            obj = int(order_NO[2:])
            orderNumber = 'UE'+str(obj+1)

            data = {
                'orderNo': orderNumber
            }
            serializer = serializers.UeOrderNumberSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                orderNumber = models.UEOrderNumber.objects.all().aggregate(Max('id'))
                return orderNumber
            else:
                data = {
                    'result': False,
                }
                return jsonResponse.error(data)
    except models.UEOrderNumber.DoesNotExist:
        # 订单号为空则新建
        print("UE1111")
        orderNumber = 'UE' + oreder_date + ord_No
        print('orderNumber', orderNumber)
        data = {
            'orderNo': orderNumber
        }
        print('data', data)
        serializer = serializers.UeOrderNumberSerializer(data=data)
        #
        # print('res_data', serializer.data)
        if serializer.is_valid():
            serializer.save()
            print('data_res', serializer.errors)
            orderNumber = models.UEOrderNumber.objects.all().aggregate(Max('id'))
            return orderNumber
        else:
            data = {
                'result': False,
                'error': serializer.errors
            }
            return jsonResponse.error(data)

