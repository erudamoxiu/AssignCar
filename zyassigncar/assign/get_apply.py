from user import models
from apply import serializers
from utils import jsonResponse


# 查询已通过审批的用车单
def approval_apply_all(apply_page_index, apply_page_size):
    # if request.method == "POST":
    try:
        pageIndex = int(apply_page_index)  # 从第几条数据开始
        pageSize = int(apply_page_size)  # 查多少条数据
    except:
        return jsonResponse.error('参数错误')
    startIndex = (pageIndex * pageSize) - pageSize
    endIndex = pageIndex * pageSize
    try:
        # 查询审批已通过的用车单approvalStatus=1
        total = models.Apply.objects.filter(approvalStatus=1).count()
        apply_all = models.Apply.objects.filter(approvalStatus=1).order_by('id')[startIndex:endIndex]
    except models.Apply.DoesNotExist:
        return jsonResponse.error('数据不存在')
    serializer = serializers.applySerializer(apply_all, many=True)
    data = {
        "data": serializer.data,
        "total": total
    }
    return data


