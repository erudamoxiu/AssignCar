from django.views.decorators.csrf import csrf_exempt
from user import models
from utils import jsonResponse
from . import serializers
from . import checkorder
from user import message_send
import datetime

# Create your views here.


# 申请用车
@csrf_exempt
def createdateApply(request):
    if request.method == 'POST':
        user = request.POST.get('userid')
        name = request.POST.get('name')
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        applyDate = datetime.datetime.now().strftime('%Y-%m-%d')
        # 判断用户是否选择目的地
        user_list = []
        destName = ''
        try:
            destId = int(request.POST.get('destId'))
        except:
            # 获取用户输入的目的地
            dest_name = request.POST.get("destname")
            destName = dest_name
            data = models.DestFee.objects.create(dest=dest_name)  # 添加到目的地费用表中
            destId = data.id  # 返回目的地id
            # 用户自主添加目的地发送通知给管理员进行补充
            approval = models.UserInfo.objects.filter(persona=1).values_list("userId", flat=True)
            approval_list = ','.join(approval)
            print('approval_list', approval_list)
            message_send.dest(approval_list, now_time, name)

        # 钉钉发送消息类型为列表
        user_list.append(user)
        """判断订单号是否存在"""
        order_no = checkorder.CheckOrderNo()
        orderNumber = order_no['id__max']
        try:
            add_data = {
                'orderNo': orderNumber,
                'orderDate': request.POST.get('useDate'),
                'userId': user,
                'applyDepart': request.POST.get('applyDepart'),
                'applyCause': request.POST.get('applyCause'),
                'applyDate': applyDate,
                'number': request.POST.get('number'),
                'phone': request.POST.get('phone'),
                'departureInfoId': request.POST.get('departureInfoId'),
                'destId': destId,
                'carNumber': request.POST.get('carNumber'),
                'carModelId': request.POST.get('carModelId'),
                'factoryId': request.POST.get('factoryId'),
                'useDate': request.POST.get('useDate'),
                'useTime': request.POST.get('useTime'),
                'createUser': user,  # 创建人
            }
        except:
            return jsonResponse.error('缺少参数')
        serializer = serializers.applySerializer(data=add_data)
        if serializer.is_valid():
            serializer.save()
            useDate = request.POST.get('useDate')
            useTime = request.POST.get('useTime')
            # 用车单提交发送钉钉提示审批通知
            approval_list = []
            approval_user = models.UserInfo.objects.filter(persona=2)
            serializer2 = serializers.UserInfoSerializer(approval_user, many=True)
            for item in serializer2.data:
                approval_list.append(item['userId'])
            approval_user = ','.join(approval_list)
            message_send.apply_approval_send(approval_user, name, now_time, useDate, useTime)

            # 申请成功发送通知给申请人
            order_n = models.OrderNumber.objects.get(id=int(orderNumber)).orderNo
            message_send.apply_message_send(user_list, order_n)
            return jsonResponse.success(True)
        else:
            # 用车单申请失败删除用户输入的目的地与用车单号
            print('errosssssssss')
            models.DestFee.objects.filter(dest=destName).delete()
            models.OrderNumber.objects.get(id=orderNumber).delete()
            return jsonResponse.error(serializer.errors)
    return jsonResponse.error('请求方式错误')


# 修改信息
@csrf_exempt
def updateApply(request):
    if request.method == 'POST':
        apply_id = request.POST.get('id')
        try:
            ap_id = models.Apply.objects.get(id=int(apply_id))
        except models.Apply.DoesNotExist:
            return jsonResponse.error('数据不存在')
        # 根据参数对数据库进行数据修改
        updata_data = {
            'orderDate': request.POST.get('orderDate'),
            'userId': request.POST.get('userId'),
            'applyDepart': request.POST.get('applyDepart'),
            'applyCause': request.POST.get('applyCause'),
            'applyDate': request.POST.get('applyDate'),
            'number': request.POST.get('number'),
            'phone': request.POST.get('phone'),
            'destId': request.POST.get('destId'),
            'orderNo': request.POST.get('orderNo'),
            'departureInfoId': request.POST.get('departureInfoId'),
            'carNumber': request.POST.get('carNumber'),
            'carModelId': request.POST.get('carModelId'),
            'factoryId': request.POST.get('factoryId'),
            'useDate': request.POST.get('useDate'),
            'useTime': request.POST.get('useTime'),
            'approvalUser': request.POST.get('approvalUser'),
            'approvalDate': request.POST.get('approvalDate'),
            'approvalOpinion': request.POST.get('approvalOpinion'),
            'approvalStatus': request.POST.get('approvalStatus'),
            # 'createUser': request.POST.get('createUser'),
            'updateUser': request.POST.get('updateUser'),
        }
        serializer = serializers.applySerializer(ap_id, data=updata_data)
        if serializer.is_valid():
            serializer.save()
            return jsonResponse.success('修改成功')
        else:
            return jsonResponse.error(serializer.errors)
    return jsonResponse.error('请求方式错误')


# 删除信息
@csrf_exempt
def deleteApply(request):
    if request.method == 'GET':
        apply_id = request.GET.get('id')
        try:
            ap_id = models.Apply.objects.get(id=int(apply_id))
        except models.Apply.DoesNotExist:
            return jsonResponse.error('数据不存在')
        ap_id.delete()
        return jsonResponse.success('删除成功')
    return jsonResponse.error('请求方式错误')


# 查询全部信息
@csrf_exempt
def getAllApply(request):
    if request.method == 'POST':
        try:
            pageIndex = int(request.POST.get('pageIndex'))
            pageSize = int(request.POST.get('pageSize'))
            status = request.POST.get('status')  # 可选
        except:
            return jsonResponse.error('参数错误')
        startIndex = (pageIndex * pageSize) - pageSize
        endIndex = pageIndex * pageSize
        try:
            if status is None or status == "":
                total = models.Apply.objects.all().count()
                apply_all = models.Apply.objects.all()[startIndex:endIndex]
            else:
                total = models.Apply.objects.filter(applyCause=status).count()
                apply_all = models.Apply.objects.filter(applyCause=status).order_by('id')[startIndex:endIndex]
        except models.Apply.DoesNotExist:
            return jsonResponse.error('数据不存在')
        serializer = serializers.applySerializer(apply_all, many=True)
        return jsonResponse.success({
            "data": serializer.data,
            "total": total
        })
    return jsonResponse.error('请求方式错误')

# 查询信息
@csrf_exempt
def getApply(request):

    if request.method == 'GET':
        apply_id = request.GET.get('id')
        try:
            ap_id = models.Apply.objects.get(id=int(apply_id))
        except models.Apply.DoesNotExist:
            return jsonResponse.error('数据不存在')
        serializer = serializers.applySerializer(ap_id)
        return jsonResponse.success(serializer.data)
    return jsonResponse.error('请求方式错误')


# 添加订单号测试数据
@csrf_exempt
def createOrderNo(request):
    if request.method == 'POST':
        ord_no = request.POST.get('ord_no')
        data = {
            'orderNo': ord_no,
            'createDate': "2018-12-31",
        }
        serializer = serializers.OrderNumberSerializer(data=data)
        serializer.is_valid()
        serializer.save()
        return jsonResponse.success(serializer.data)


# 展示所有未审批的用车单
@csrf_exempt
def approval_apply_all(request):
    if request.method == "POST":
        try:
            pageIndex = int(request.POST.get('pageIndex'))  # 从第几条数据开始
            pageSize = int(request.POST.get('pageSize'))  # 查多少条数据
        except:
            return jsonResponse.error('参数错误')
        startIndex = (pageIndex * pageSize) - pageSize
        endIndex = pageIndex * pageSize
        try:
            total = models.Apply.objects.filter(approvalStatus=0).count()
            apply_all = models.Apply.objects.filter(approvalStatus=0).order_by('id')[startIndex:endIndex]
        except models.Apply.DoesNotExist:
            return jsonResponse.error('数据不存在')
        serializer = serializers.applySerializer(apply_all, many=True)
        return jsonResponse.success({
            "data": serializer.data,
            "total": total
        })
    return jsonResponse.error('请求方式错误')


# 审核
@csrf_exempt
def approval_apply(request):
    if request.method == 'POST':
        apply_id = request.POST.get('id')
        user = request.POST.get('updateUser')
        statu = request.POST.get('status')
        approvalOpinion = request.POST.get('approvalOpinion')
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        try:
            ap_id = models.Apply.objects.get(id=int(apply_id))
            orderNo = ap_id.orderNo.orderNo
        except models.Apply.DoesNotExist:
            return jsonResponse.error('数据不存在')
        updata_data = {
            'approvalStatus': statu,
            'approvalOpinion': approvalOpinion,
            'updateUser': user,
            'approvalUserId': user,
            'approvalDate': now_time
        }
        serializer = serializers.ApprovalChange(ap_id, data=updata_data)
        if serializer.is_valid():
            serializer.save()
            user_list = []
            assign_list = []

            if statu == "2":
                # 发送审核不通过通知给申请人
                user_data = models.Apply.objects.get(id=int(apply_id)).serializable_value('userId')
                user_list.append(user_data)
                message_send.approval_veto_send(user_list, orderNo, approvalOpinion)
                print('不通过')

            elif statu == "1":
                # 发送审核通过通知给申请人
                user_data = models.Apply.objects.get(id=int(apply_id)).serializable_value('userId')
                name = models.UserInfo.objects.get(userId=user_data).serializable_value('name')
                user_list.append(name)
                message_send.approval_pass_send(user_list, orderNo)

                # 发送通知给派车员分派车辆 找到用户表中所有的派车员
                try:
                    assign_user = models.UserInfo.objects.filter(persona=3)
                except:
                    return jsonResponse.error('无派车员')
                serializer2 = serializers.UserInfoSerializer(assign_user, many=True)
                for item in serializer2.data:
                    assign_list.append(item['userId'])
                user_lis = ','.join(assign_list)
                message_send.assign_car(user_lis, name)
            return jsonResponse.success(True)
        else:
            return jsonResponse.error(serializer.errors)
    return jsonResponse.error('请求方式错误')


# 展示所有已审批通过的用车单
@csrf_exempt
def approval_pass_all(request):
    if request.method == "POST":
        try:
            pageIndex = int(request.POST.get('pageIndex'))  # 从第几条数据开始
            pageSize = int(request.POST.get('pageSize'))  # 查多少条数据
        except:
            return jsonResponse.error('参数错误')
        startIndex = (pageIndex * pageSize) - pageSize
        endIndex = pageIndex * pageSize
        try:
            total = models.Apply.objects.filter(approvalStatus=1).count()
            apply_all = models.Apply.objects.filter(approvalStatus=1).order_by('id')[startIndex:endIndex]
        except models.Apply.DoesNotExist:
            return jsonResponse.error('数据不存在')
        serializer = serializers.applySerializer(apply_all, many=True)
        return jsonResponse.success({
            "data": serializer.data,
            "total": total
        })
    return jsonResponse.error('请求方式错误')