import requests
from user import get_token

userid = ['manager8217']


def approval_send(form_component_values):
    access_token = get_token.is_time()
    url = 'https://oapi.dingtalk.com/topapi/processinstance/create?access_token=%s' % access_token
    payload = {
        "agent_id": 210527492,
        "process_code": "PROC-0KYJ80KV-48S1NOB4Y0T071DJ83RV2-LU8HJGQJ-8",
        "originator_user_id": 'manager8217',
        "dept_id": -1,
        "approvers": userid,
        "form_component_values": form_component_values
    }
    res_data = requests.post(url, params=payload)
    res = res_data.json()
    print("res", res)
