import requests
from user import get_token
import json

userid = ['manager8217']


# 发送用车申请审批消息
def apply_approval_send(user_list, name, now_time, useDate, useTime):
    access_token = get_token.is_time()
    url = 'https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2?access_token=%s' % access_token
    message_msg = {
        "msgtype": "text",
        "text": {
            "content": "用户 %s 于 %s 申请用车，用车时间为: %s %s，请前往进行审批。" % (name, now_time, useDate, useTime)  # 加上使用时间
        }
    }
    msg = json.dumps(message_msg)
    payload = {
        "agent_id": 210527492,
        "userid_list": user_list,
        "msg": msg
    }
    res_data = requests.post(url, params=payload)
    res = res_data.json()
    print("res", res)


# 发送用车申请提交消息
def apply_message_send(user_list, order_no):
    access_token = get_token.is_time()
    url = 'https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2?access_token=%s' % access_token
    message_msg = {
        "msgtype": "text",
        "text": {
            "content": "提交用车申请成功，您的申请单号为%s，请等待管理员审批。" % order_no
        }
    }
    msg = json.dumps(message_msg)
    payload = {
        "agent_id": 210527492,
        "userid_list": user_list,
        "msg": msg
    }
    res_data = requests.post(url, params=payload)
    res_data.json()


# 发送审批通过消息
def approval_pass_send(user_list, orderNo):
    access_token = get_token.is_time()
    url = 'https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2?access_token=%s' % access_token
    message_msg = {
        "msgtype": "text",
        "text": {
            "content": "您的用车申请,单号:%s已经通过审批，请等待派车。" % orderNo
        }
    }
    msg = json.dumps(message_msg)
    payload = {
        "agent_id": 210527492,
        "userid_list": user_list,
        "msg": msg
    }
    res_data = requests.post(url, params=payload)
    res = res_data.json()
    print("res", res)


# 发送审批不通过消息
def approval_veto_send(user_list, orderNo, approvalOpinion):
    access_token = get_token.is_time()
    url = 'https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2?access_token=%s' % access_token
    message_msg = {
        "msgtype": "text",
        "text": {
            "content": "很遗憾，您的用车申请,单号:%s未能通过审核，审核理由为: %s" % (orderNo, approvalOpinion)  # 加上拒绝理由
        }
    }
    msg = json.dumps(message_msg)
    payload = {
        "agent_id": 210527492,
        "userid_list": user_list,
        "msg": msg
    }
    res_data = requests.post(url, params=payload)
    res = res_data.json()
    print("res", res)


# 派车成功发送通知给用户
def assign_pass_send(user_list, assign_order_no, departureDate, departureTime, departure_message, carModelStr, lic_str, driver_name, phone_str, destfee):
    access_token = get_token.is_time()
    url = 'https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2?access_token=%s' % access_token
    message_msg = {
        "msgtype": "text",
        "text": {
            "content": "派车成功!请按出发时间准时前往出发地，谢谢。\n派车单号: %s\n出发时间: %s %s\n出发地: %s\n车型/车牌: %s/%s\n司机/电话号码: %s/%s\n目的地: %s" % (assign_order_no, departureDate, departureTime, departure_message, carModelStr, lic_str, driver_name, phone_str, destfee)
        }
    }

    msg = json.dumps(message_msg)
    payload = {
        "agent_id": 210527492,
        "userid_list": user_list,
        "msg": msg
    }
    res_data = requests.post(url, params=payload)
    res = res_data.json()
    print('res', res)


# 通知管理员补充目的的资料
def dest(user_list, now_time, name):
    access_token = get_token.is_time()
    url = 'https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2?access_token=%s' % access_token
    message_msg = {
        'msgtype': 'text',
        'text': {
            "content": '用户 %s 在%s 申请用车时添加了新的目的地，请前往进行对资料的补充' % (name, now_time)  # 加上用户创建用车单的时间 防止管理员因钉钉通知限制收不到通知
        }
    }

    msg = json.dumps(message_msg)
    payload = {
        "agent_id": 210527492,
        "userid_list": user_list,
        "msg": msg
    }
    requests.post(url, params=payload)


# 通知派车员进行车辆分派
def assign_car(assign_list, name):
    access_token = get_token.is_time()
    url = 'https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2?access_token=%s' % access_token
    message_msg = {
        'msgtype': 'text',
        'text': {
            "content": '用户 %s 的用车审核已通过审核，请前往进行分派车辆===' % name
        }
    }

    msg = json.dumps(message_msg)
    payload = {
        "agent_id": 210527492,
        "userid_list": assign_list,
        "msg": msg
    }
    res = requests.post(url, params=payload)
    print('res', res)


# 司机提交回程单成功通知
def return_data(user_list, orderNo):
    access_token = get_token.is_time()
    url = 'https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2?access_token=%s' % access_token
    message_msg = {
        'msgtype': 'text',
        'text': {
            "content": '您的单号: %s 回程单提交成功，请等待审核，谢谢!' % orderNo
        }
    }

    msg = json.dumps(message_msg)
    payload = {
        "agent_id": 210527492,
        "userid_list": user_list,
        "msg": msg
    }
    requests.post(url, params=payload)


# 发送回程单审核通知
def return_order(approval, user, now_time):
    access_token = get_token.is_time()
    url = 'https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2?access_token=%s' % access_token
    message_msg = {
        'msgtype': 'text',
        'text': {
            "content": '用户 %s 于 %s 提交车辆回程单，请前往进行审核。' % (user, now_time)
        }
    }

    msg = json.dumps(message_msg)
    payload = {
        "agent_id": 210527492,
        "userid_list": approval,
        "msg": msg
    }
    requests.post(url, params=payload)


# 回程审核通过通知
def return_pass(user_list, orderNo):
    access_token = get_token.is_time()
    url = 'https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2?access_token=%s' % access_token
    message_msg = {
        "msgtype": "text",
        "text": {
            "content": "您的派车单号: %s 已经通过回程审核。" % orderNo
        }
    }
    msg = json.dumps(message_msg)
    payload = {
        "agent_id": 210527492,
        "userid_list": user_list,
        "msg": msg
    }
    requests.post(url, params=payload)


# 回程审核不通过消息
def return_veto_send(user_list, orderNo, approvalOpinion):
    access_token = get_token.is_time()
    url = 'https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2?access_token=%s' % access_token
    message_msg = {
        "msgtype": "text",
        "text": {
            "content": "很遗憾，您的用车申请,单号:%s未能通过审核，审核理由为:%s" % (orderNo, approvalOpinion)  # 加上拒绝理由
        }
    }
    msg = json.dumps(message_msg)
    payload = {
        "agent_id": 210527492,
        "userid_list": user_list,
        "msg": msg
    }
    res_data = requests.post(url, params=payload)