# Create your views here.
from django.http import HttpResponse
from user import config, models
from . import get_token, ddVaild, sign, serializers
from utils import jsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from django.db.models import Q

AppInfo = config.AppInfo()
Vaild = ddVaild.Vaild()


def test(request):
    return HttpResponse('success!!!')

# 判断用户是否存在
def isUser(userId):
    try:
        user = models.UserInfo.objects.get(userId=userId)
    except models.UserInfo.DoesNotExist:
        return HttpResponse('user does not exist', status=404)
    return user


# 验证
@csrf_exempt
def getJSAPI(request):
    try:
        path = request.META['HTTP_REFERER']
    except:
        return jsonResponse.error('无法获取当前URL地址')
    ticket = Vaild.getTicket()
    try:
        if "error" in ticket:
            return jsonResponse.error(ticket['error'])
    except:
        pass
    sign1 = sign.Sign(ticket, path)
    result = sign1.sign()
    result['agentId'] = AppInfo.AgentId
    result['corpId'] = AppInfo.CorpId
    newData = {
        'data': result
    }
    return jsonResponse.success(newData)


# 通过Code获取当前用户的详细信息 自动添加用户支数据库
@csrf_exempt
def getUserInfo(request):
    if request.method == 'GET':
        code = request.GET.get('code')
        access_token = get_token.is_time()
        url = 'https://oapi.dingtalk.com/user/getuserinfo'
        payload = {'access_token': access_token, 'code': code}
        res_data = requests.get(url, params=payload)
        res = res_data.json()

        if 'userid' in res:
            try:
                # 已存在的用户直接返回
                users = models.UserInfo.objects.get(userId=res['userid'])
            except:
                # 第一次使用的用户添加到数据库中
                params2 = {
                    'access_token': access_token,
                    'userid': res['userid']
                }
                res = requests.get('https://oapi.dingtalk.com/user/get', params=params2,
                                   headers={'Connection': 'close'})
                res1 = res.json()
                add_data = {
                    'userId': res1['userid'],
                    'name': res1['name'],
                    'type': 0,
                    'department': ','.join(map(str, res1['department'])),
                    'position': res1['position'] if 'position' in res1 else '',
                    'avatar': res1['avatar'],
                    'jobNumber': res1['jobNumber'] if 'jobNumber' in res1 else '',
                }
                serializer = serializers.UserInfoSerializer(data=add_data)
                serializer.is_valid()
                serializer.save()
                return jsonResponse.success(serializer.data)
            serializer = serializers.UserInfoSerializer(users)
            ser = serializer.data
            # 获取部门名字
            id = ser['department']
            payload = {'access_token': access_token, 'id': id}
            res = requests.get('https://oapi.dingtalk.com/department/get', params=payload)
            res1 = res.json()
            ser['departmentName'] = res1['name']
            return jsonResponse.success(ser)
        else:
            return jsonResponse.error(res['errmsg'])
    return jsonResponse.error('请求方式错误')


# 添加用户
@csrf_exempt
def addUser(request):
    if request.method == 'POST':
        userIds = request.POST.get('userIds').split(',')        # 字符串转列表
        userType = request.POST.get('userType')
        createUser = request.POST.get('createUser')

        if userIds is None or userType is None:
             return jsonResponse.error('Parameter error!')
        access_token = get_token.is_time()
        try:
            if "error" in access_token:
                return jsonResponse.error(access_token['error'])
        except:
            pass
        try:
            # 用户已存在，修改角色类型
            for item in userIds:
                user = models.UserInfo.objects.get(userId=item)
                user.persona = userType
                user.updateUser = createUser
                user.save()
            return jsonResponse.success(True)
        except:
            # 不存在则新建
            for item in userIds:
                params2 = {
                    'access_token': access_token,
                    'userid': item,
                }
                res = requests.get('https://oapi.dingtalk.com/user/get', params=params2, headers={'Connection':'close'})
                res1 = res.json()
                if 'errcode' in res:
                    return jsonResponse.error('The user could not be found')
                add_data = {
                    'userId': res1['userid'],
                    'name': res1['name'],
                    'persona': userType,
                    'department': ','.join(map(str, res1['department'])),
                    'position': res1['position'] if 'position' in res1 else '',
                    'avatar': res1['avatar'],
                    'jobNumber': res1['jobNumber'] if 'jobNumber' in res1 else '',
                    'createUser': createUser,
                }
                serializer = serializers.UserInfoSerializer(data=add_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    pass
            return jsonResponse.success(True)
    return jsonResponse.error('page not found')


# 分页查询用户
# 根据用户类型返回对应的用户数组
@csrf_exempt
def getUser(request):
    if request.method == 'POST':
        try:
            pageIndex = int(request.POST.get('pageIndex'))  # 必须
            pageSize = int(request.POST.get('pageSize'))    # 必须
            userType = int(request.POST.get('type'))        # 必须
            keyWord = request.POST.get('keyWord')           # 可选
        except:
            return jsonResponse.error('参数错误')
        startIndex = (pageIndex * pageSize) - pageSize      # 开始查询索引
        endIndex = pageIndex * pageSize                     # 结束查询索引

        try:
            if keyWord == '' or keyWord is None:
                total = models.UserInfo.objects.filter(persona=userType).count()
                users = models.UserInfo.objects.filter(persona=userType)[startIndex:endIndex]
            else:
                #  按关键字分页查询   可模糊查询 resellerCode和resellerName的值
                query = Q()
                q1 = Q()
                q1.connector = "AND"  # 连接的条件是AND 代表就是&
                q1.children.append(("persona", userType))           # persona代表的是数据库的字段
                q1.children.append(("name__contains", keyWord))     # name__contains代表模糊查询name字段
                q2 = Q()
                q2.connector = "AND"  # 连接的条件是AND 代表就是&
                q2.children.append(("persona", userType))           # type代表的是数据库的字段
                q2.children.append(("userId__contains", keyWord))   # userId__contains代表模糊查询userId字段
                query.add(q1, "OR")
                query.add(q2, "OR")
                total = models.UserInfo.objects.filter(query).count()
                users = models.UserInfo.objects.filter(query)[startIndex:endIndex]
        except models.UserInfo.DoesNotExist:
            return jsonResponse.error('user does not exist')
        serializer = serializers.UserInfoSerializer(users, many=True)
        return jsonResponse.success({
            "total": total,
            "data": serializer.data
        })
    return jsonResponse.error('page not found')


# 获取用户详细信息
@csrf_exempt
def getUserDetail(request):
    if request.method == 'GET':
        userId = request.GET.get('userId')
        users = models.UserInfo.objects.get(userId=userId)
        serializer = serializers.UserInfoSerializer(users)
        # ser = serializer.data
        # id = serializer.data['department']
        # # 获取部门名字
        # access_token = get_token.is_time()
        # payload = {'access_token': access_token, 'id': id}
        # res = requests.get('https://oapi.dingtalk.com/department/get', params=payload)
        # res1 = res.json()
        # ser['departmentName'] = res1['name']
        # print(ser)
        return jsonResponse.success(serializer.data)
    return jsonResponse.error('请求方式错误')


# 修改用户
@csrf_exempt
def updateUser(request):
    if request.method == 'POST':
        persona = request.POST.get('persona')   # 修改角色类型
        userId = request.POST.get('userId')     # 要修改的用户
        updateUser = request.POST.get('name')   # 修改人
        try:
            user = models.UserInfo.objects.get(userId=userId)
        except models.UserInfo.DoesNotExist:
            return jsonResponse.error('用户不存在')
        user.persona = persona
        user.updateUser = updateUser
        user.save()
        return jsonResponse.success(True)
    return jsonResponse.error('请求方式错误')


# 删除用户
@csrf_exempt
def deleteUser(request):
    if request.method == 'GET':
        userId = request.GET.get('userId')
        user = isUser(userId)
        user.delete()
        return jsonResponse.success(True)
    return jsonResponse.error('page not found')







