from rest_framework import serializers
from user.models import Apply, OrderNumber, UserInfo


class applySerializer(serializers.ModelSerializer):
    factory_name = serializers.ReadOnlyField(source='factoryId.factoryName', read_only=True)
    carModel = serializers.ReadOnlyField(source='carModelId.carModel', read_only=True)
    departure = serializers.ReadOnlyField(source='departureInfoId.departure', read_only=True)
    dest = serializers.ReadOnlyField(source='destId.dest', read_only=True)
    channel = serializers.ReadOnlyField(source='destId.channel', read_only=True)
    order_no = serializers.ReadOnlyField(source='orderNo.orderNo', read_only=True)
    applyUser = serializers.ReadOnlyField(source='userId.name', read_only=True)
    # Status = serializers.ReadOnlyField(source='approvalStatus', read_only=True)
    """
    出发地详细信息序列化器
    """
    class Meta:
        model = Apply
        fields = ['id',
                  'orderNo',
                  'order_no',
                  'orderDate',
                  'userId',
                  'applyUser',
                  'applyDepart',
                  'applyCause',
                  'applyDate',
                  'number',
                  'phone',
                  'departureInfoId',
                  'departure',
                  'destId',
                  'dest',
                  'channel',
                  'carNumber',
                  'carModelId',
                  'carModel',
                  'factoryId',
                  'factory_name',
                  'useDate',
                  'useTime',
                  'approvalUserId',
                  'approvalDate',
                  'approvalOpinion',
                  'approvalStatus',
                  'createUser',
                  'updateUser'
        ]


class OrderNumberSerializer(serializers.ModelSerializer):
    """
    订单号
    """
    class Meta:
        model = OrderNumber
        fields = [
            'id',
            'orderNo',
            'createDate'
        ]


class ApprovalChange(serializers.ModelSerializer):
    """
    修改审核状态
    """
    class Meta:
        model = Apply
        fields = ['approvalStatus',
                  'approvalOpinion',
                  'updateUser',
                  'approvalUserId',
                  'approvalDate',
                  ]


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['id', 'userId', 'openId', 'name', 'position', 'avatar', 'jobNumber', 'createUser', 'updateUser', 'persona']