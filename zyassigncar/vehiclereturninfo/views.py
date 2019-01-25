from django.views.decorators.csrf import csrf_exempt
from user import models
from utils import jsonResponse
from . import serializers
from user import message_send
import datetime
# Create your views here.


# 创建车辆回程信息
@csrf_exempt
def createVehicleReturn(request):
    if request.method == 'POST':
        user = request.POST.get('userid')
        user_list = []
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        try:
            data = {
                'assignDetail2Id': request.POST.get('id'),
                'carStartDate': request.POST.get('carStartDate'),
                'carStartTime': request.POST.get('carStartTime'),
                'carReturnDate': request.POST.get('carReturnDate'),
                'carReturnTime': request.POST.get('carReturnTime'),
                'startMileage': request.POST.get('startMileage'),
                'returnMileage': request.POST.get('returnMileage'),
                'oilVolume': request.POST.get('oilVolume'),
                'toll': request.POST.get('toll'),
                'parkingFee': request.POST.get('parkingFee'),
                'expresswayFee': request.POST.get('expresswayFee'),
                'overtime': request.POST.get('overtime'),
                'mealFee': request.POST.get('mealFee'),
                'otherFee': request.POST.get('otherFee'),
                'remark': request.POST.get('remark'),
                'createUser': request.POST.get('createUser'),
            }
            serializer = serializers.ReturnOrderSerializer(data=data)
        except:
            return jsonResponse.error('参数错误')
        try:
            serializer.is_valid()
            serializer.save()
        except Exception as e:
            return jsonResponse.error(e)
        # 修改司机回程单状态
        obj = models.AssignDetail2.objects.get(id=int(data['assignDetail2Id']))
        driver_name = obj.driverId.driverName.name
        obj.type = "1"
        obj.save()
        # 发送提交回程单成功通知给司机
        user_list.append(user)
        ser = serializers.Detail2Serializer(obj)
        orderNo = ser.data['orderNo']
        message_send.return_data(user_list, orderNo)

        # 发送通知给审核员
        approval = models.UserInfo.objects.filter(persona=2).values_list("userId", flat=True)
        approval_list = ','.join(approval)
        message_send.return_order(approval_list, driver_name, now_time)  # 司机姓名
        return jsonResponse.success(True)
    return jsonResponse.error('请求错误')


# 单个车辆回程表
@csrf_exempt
def getVehicleReturn(request):
    if request.method == 'GET':
        try:
            veh_id = request.GET.get('id')
            veh_data = models.ReturnOrder.objects.get(id=int(veh_id))
        except models.ReturnOrder.DoesNotExist:
            return jsonResponse.error('数据不存在')
        serializer = serializers.ReturnOrderSerializer(veh_data)
        veh_ser_data = serializer.data
        detail2_id = veh_ser_data['assignDetail2Id']  # 从回程表中获取明细表2id

        # 序列化明细2表
        detail2 = models.AssignDetail2.objects.get(id=detail2_id)
        detail2_data = serializers.Detail2Serializer(detail2)
        d2 = detail2_data.data
        detail1_id = d2['assignId']  # 获取派车单id

        # 序列化明细1表
        detail1 = models.AssignDetail1.objects.filter(assignId=detail1_id)
        detail1_data = serializers.Detail1Serializer(detail1, many=True)
        d1 = detail1_data.data[0]

        # 整合返回数据
        dict_data = {}
        for item1 in d1:
            dict_data[item1] = d1[item1]
        for item2 in d2:
            dict_data[item2] = d2[item2]
        for item in veh_ser_data:
            dict_data[item] = veh_ser_data[item]
        return jsonResponse.success(dict_data)
    return jsonResponse.error('请求方式错误')


# 查询全部填写的回程表
@csrf_exempt
def getAllVehicleReturn(request):
    if request.method == 'POST':
        try:
            pageIndex = int(request.POST.get('pageIndex'))
            pageSize = int(request.POST.get('pageSize'))
        except:
            return jsonResponse.error('参数错误')
        startIndex = (pageIndex * pageSize) - pageSize
        endIndex = pageIndex * pageSize
        try:
            total = models.ReturnOrder.objects.filter(approvalStatus=0).count()
            print('total', total)
            vehicle_all = models.ReturnOrder.objects.filter(approvalStatus=0).order_by('id')[startIndex:endIndex]
        except models.ReturnOrder.DoesNotExist:
            return jsonResponse.error('数据不存在')
        serializer = serializers.ReturnOrderSerializer(vehicle_all, many=True)
        vehicle_data = serializer.data
        print('ver', vehicle_data)
        return jsonResponse.success({
            'data': vehicle_data,
            'total': total
        })
    return jsonResponse.error('请求错误')


# 修改回程表
@csrf_exempt
def updateVehicleReturn(request):
    if request.method == 'POST':
        try:
            veh_id = request.POST.get('id')
            veh_data = models.ReturnOrder.objects.get(id=int(veh_id))
        except models.ReturnOrder.DoesNotExist:
            return jsonResponse.error('数据不存在')
        updata = {
            'startMileage': request.POST.get('startmileage'),
            'returnMileage': request.POST.get('returnmileage'),
            'oilVolume': request.POST.get('oilvolume'),
            'toll': request.POST.get('toll'),
            'parkingFee': request.POST.get('parkingfee'),
            'expresswayFee': request.POST.get('expresswayfee'),
            'overtime': request.POST.get('overtime'),
            'mealFee': request.POST.get('mealfee'),
            'otherFee': request.POST.get('otherfee'),
            'remark': request.POST.get('remark'),
            'approvalUser': request.POST.get('name'),
            'updateUser': request.POST.get('userid'),
        }
        serializer = serializers.ReturnOrderSerializer(veh_data, data=updata)
        if serializer.is_valid():
            serializer.save()
            return jsonResponse.success('修改成功')
        else:
            return jsonResponse.error(serializer.errors)
    return jsonResponse.error('请求方式错误')


# 展示所有分派的用车单
@csrf_exempt
def show_all_apply(request):
    if request.method == "POST":
        try:
            pageIndex = int(request.POST.get('pageIndex'))  # 从第几条数据开始
            pageSize = int(request.POST.get('pageSize'))  # 查多少条数据
        except:
            return jsonResponse.error('参数错误')
        startIndex = (pageIndex * pageSize) - pageSize
        endIndex = pageIndex * pageSize
        try:
            total = models.AssignDetail2.objects.all().count()
            apply_all = models.AssignDetail2.objects.all()[startIndex:endIndex]
        except models.AssignDetail2.DoesNotExist:
            return jsonResponse.error('数据不存在')
        serializer = serializers.Detail2Serializer(apply_all, many=True)
        return jsonResponse.success({
            "data": serializer.data,
            "total": total
        })
    return jsonResponse.error('请求方式错误')


# 查询单条回程单填写
@csrf_exempt
def show_assign(request):
    if request.method == 'GET':
        try:
            id = request.GET.get('id')
            # 用户一进入使用用户接口获取userid 从用户表中找到名字再去明细２表中查找对应的派车单，结合关联的用车单一起展示单张需要司机填写的回程表首页
            detail2 = models.AssignDetail2.objects.get(id=int(id))
            serializer = serializers.Detail2Serializer(detail2)
            # 明细2数据
            detail2_data = serializer.data
            as_id = detail2_data['assignId']
            assign = models.Assign.objects.get(id=int(as_id))
            assign_data = serializers.AssignSerializer(assign)
            ass = assign_data.data
            detail1 = models.AssignDetail1.objects.filter(assignId=as_id)
            # 明细1数据
            datail1_data = serializers.Detail1Serializer(detail1, many=True)
            datail1_ser = datail1_data.data[0]

            # 整合数据
            dict_data = {}
            for item in ass:
                dict_data[item] = ass[item]
            for item1 in datail1_ser:
                dict_data[item1] = datail1_ser[item1]
            for item2 in detail2_data:
                dict_data[item2] = detail2_data[item2]

            return jsonResponse.success(dict_data)
        except Exception as e:
            return jsonResponse.error(e)
    else:
        return jsonResponse.error('数据不存在')


# 展示所有待审核回程单
@csrf_exempt
def show_approval_vchiclereturn(request):
    if request.method == 'POST':
        try:
            pageIndex = int(request.POST.get('pageIndex'))  # 从第几条数据开始
            pageSize = int(request.POST.get('pageSize'))  # 查多少条数据
        except:
            return jsonResponse.error('参数错误')
        startIndex = (pageIndex * pageSize) - pageSize
        endIndex = pageIndex * pageSize
        try:
            total = models.ReturnOrder.objects.filter(approvalStatus=0).count()
            vchiclereTurn_all = models.ReturnOrder.objects.filter(approvalStatus=0)[startIndex:endIndex]
        except models.Apply.DoesNotExist:
            return jsonResponse.error('数据不存在')
        serializer = serializers.ReturnOrderSerializer(vchiclereTurn_all, many=True)
        return jsonResponse.success({
            "data": serializer.data,
            "total": total
        })
    return jsonResponse.error('请求方式错误')


# 审核
@csrf_exempt
def approval_vchiclereturn(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        user = request.POST.get('approvalUser')  # 审核员
        statu = request.POST.get('status')
        approvalExplanation = request.POST.get('approvalExplanation')
        try:
            ap_id = models.ReturnOrder.objects.get(id=int(id))
        except models.Apply.DoesNotExist:
            return jsonResponse.error('数据不存在')
        updata_data = {
            'approvalStatus': statu,
            'approvalExplanation': approvalExplanation,
            'approvalUser': user,
            'updateUser': user,
        }
        serializer = serializers.ReturnOrderApprovaSerializer(ap_id, data=updata_data)
        if serializer.is_valid():
            serializer.save()
            user_list = []

            detail_id = models.ReturnOrder.objects.get(id=int(id)).serializable_value('assignDetail2Id')
            # 审核后发送通知 获取司机的userid
            obj = models.AssignDetail2.objects.get(id=int(detail_id))
            ser = serializers.Detail2Serializer(obj)
            orderNo = ser.data['orderNo']
            driver_id = ser.data['driverId']
            driver_name = models.Driver.objects.get(id=int(driver_id)).serializable_value('driverName')
            user_list.append(driver_name)  # 司机userid

            if statu == "2":
                # 司机回程单改为未填写让其重新填写
                obj = models.AssignDetail2.objects.get(id=int(detail_id))
                obj.type = "0"
                obj.save()
                # 发送拒审消息和原因，提示司机重新填写回程单
                message_send.approval_veto_send(user_list, orderNo, approvalExplanation)

                # 将回程单删除-司机重新创建回程单
                models.ReturnOrder.objects.get(id=int(id)).delete()

            elif statu == "1":
                # 审核通过发送通知给司机
                message_send.return_pass(user_list, orderNo)
            return jsonResponse.success(True)
        else:
            return jsonResponse.error(serializer.errors)
    return jsonResponse.error('请求方式错误')


# 司机所有的派车任务 页面入口
@csrf_exempt
def driver_data_all(request):
    if request.method == 'POST':
        driver_name = request.POST.get('tableData')
        try:
            pageIndex = int(request.POST.get('pageIndex'))
            pageSize = int(request.POST.get('pageSize'))
        except:
            return jsonResponse.error('参数错误')
        startIndex = (pageIndex * pageSize) - pageSize
        endIndex = pageIndex * pageSize
        try:
            # 司机派车任务数量(明细2)
            total = models.AssignDetail2.objects.filter(driverId__driverName=driver_name, type=0).count()
            # 根据创建时间排序 最新的数据显示在最上方
            vehicle_all = models.AssignDetail2.objects.filter(driverId__driverName=driver_name, type=0).order_by('id')[startIndex:endIndex]
        except models.ReturnOrder.DoesNotExist:
            return jsonResponse.error('数据不存在')
        detail2 = serializers.Detail2Serializer(vehicle_all, many=True)
        detail2_data = detail2.data

        return jsonResponse.success({
            'data': detail2_data,
            'total': total,
        })
    return jsonResponse.error('请求错误')
