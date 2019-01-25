from user import models
from carinfo import serializers
from utils import jsonResponse


# 查询全部车辆信息
def get_carinfo_all(car_page_index, car_page_size):
    try:
        pageIndex = int(car_page_index)  # 从第几条数据开始
        pageSize = int(car_page_size)  # 查多少条数据
    except:
        return jsonResponse.error('参数错误')
    startIndex = (pageIndex * pageSize) - pageSize
    endIndex = pageIndex * pageSize
    try:
        total = models.CarInfo.objects.all().count()
        car_all = models.CarInfo.objects.all()[startIndex:endIndex]
    except models.CarInfo.DoesNotExist:
        return jsonResponse.error('数据不存在')
    serializer = serializers.carInfoSerializer(car_all, many=True)
    data = {
        "data": serializer.data,
        "total": total
    }
    return data
