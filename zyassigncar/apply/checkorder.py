import datetime
from user import models
from utils import jsonResponse
from . import serializers
from django.db.models import Max


# 检查单号
def CheckOrderNo():
    oreder_date = datetime.datetime.now().strftime("%Y%m%d")
    ord_No = '0001'
    try:
        orderNo = models.OrderNumber.objects.all().aggregate(Max('id'))
        # 通过最大值找到对应数据
        orde_no = models.OrderNumber.objects.get(id=orderNo['id__max'])
        # 最大订单号实例化
        order_NO = orde_no.orderNo
        # 取出时间进行类型转换
        orderNo_datetime = orde_no.createDate.strftime("%Y%m%d")

        # 判断当前时间是否大于创建时间
        if int(oreder_date) > int(orderNo_datetime):
            # 重置订单号
            orderNumber = 'AP'+oreder_date + ord_No
            data = {
                'orderNo': orderNumber
            }
            serializer = serializers.OrderNumberSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                orderNumber = models.OrderNumber.objects.all().aggregate(Max('id'))
                return orderNumber
            else:
                data = {
                    'result': False,
                }
                return jsonResponse.error(data)
        else:
            # 如果是当天创建则找到最大订单号+1
            obj = int(order_NO[2:])
            orderNumber = 'AP'+str(obj+1)

            data = {
                'orderNo': orderNumber
            }
            serializer = serializers.OrderNumberSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                orderNumber = models.OrderNumber.objects.all().aggregate(Max('id'))
                return orderNumber
            else:
                data = {
                    'result': False,
                }
                return jsonResponse.error(data)
    except models.OrderNumber.DoesNotExist:
        # 订单号为空则新建
        orderNumber = 'AP' + oreder_date + ord_No
        data = {
            'orderNo': orderNumber
        }
        serializer = serializers.OrderNumberSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            orderNumber = models.OrderNumber.objects.all().aggregate(Max('id'))
            return orderNumber
        else:
            data = {
                'result': False,
            }
            return jsonResponse.error(data)

