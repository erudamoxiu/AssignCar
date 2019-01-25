from rest_framework import serializers
from user.models import ReturnOrder, AssignDetail1, AssignDetail2, Apply, Assign


class ReturnOrderSerializer(serializers.ModelSerializer):
    licensePlate = serializers.ReadOnlyField(source='assignDetail2Id.carInfoId.licensePlate', read_only=True)
    driverName = serializers.ReadOnlyField(source='assignDetail2Id.driverId.driverName.name', read_only=True)
    driverPhone = serializers.ReadOnlyField(source='assignDetail2Id.driverId.phone', read_only=True)
    orderNo = serializers.ReadOnlyField(source='assignDetail2Id.assignId.orderNo.orderNo', read_only=True)

    """
    车辆回程信息序列化器
    """
    class Meta:
        model = ReturnOrder
        fields = (
            'id',
            'orderNo',
            'assignDetail2Id',
            'carStartDate',
            'carStartTime',
            'carReturnDate',
            'carReturnTime',
            'startMileage',
            'returnMileage',
            'oilVolume',
            'toll',
            'parkingFee',
            'expresswayFee',
            'overtime',
            'mealFee',
            'otherFee',
            'remark',
            'approvalUserId',
            'approvalDate',
            # 'approvalStatus',
            'licensePlate',
            'driverName',
            'driverPhone',
            'createUser',
            'updateUser',
        )


class ReturnOrderApprovaSerializer(serializers.ModelSerializer):
    """
    审核回程单
    """
    class Meta:
        model = ReturnOrder
        fields = (
            'approvalStatus',
            'approvalExplanation',
            'approvalUserId',
            'updateUser',
        )


class Detail1Serializer(serializers.ModelSerializer):
    applyUser = serializers.ReadOnlyField(source='applyId.userId.name', read_only=True)
    applyDepart = serializers.ReadOnlyField(source='applyId.applyDepart', read_only=True)
    phone = serializers.ReadOnlyField(source='applyId.phone', read_only=True)
    applyCause = serializers.ReadOnlyField(source='applyId.applyCause', read_only=True)
    useDate = serializers.ReadOnlyField(source='applyId.useDate', read_only=True)
    useTime = serializers.ReadOnlyField(source='applyId.useTime', read_only=True)
    number = serializers.ReadOnlyField(source='applyId.number', read_only=True)
    carNumber = serializers.ReadOnlyField(source='applyId.carNumber', read_only=True)
    departure = serializers.ReadOnlyField(source='applyId.departureInfoId.departure', read_only=True)
    approvalOpinion = serializers.ReadOnlyField(source='applyId.approvalOpinion', read_only=True)
    factoryName = serializers.ReadOnlyField(source='applyId.factoryId.factoryName', read_only=True)
    # carModel = serializers.ReadOnlyField(source='applyId.carModelId.carModel', read_only=True)
    dest = serializers.ReadOnlyField(source='applyId.destId.dest', read_only=True)
    channel = serializers.ReadOnlyField(source='applyId.destId.channel', read_only=True)
    """
    明细表1
    """
    class Meta:
        model = AssignDetail1
        fields = [
            'id',
            'assignId',
            'applyId',
            'applyUser',  # 申请人
            'applyDepart',  # 申请部门
            'phone',  # 电话
            'applyCause',  # 申请事由
            'useDate',  # 使用日期
            'useTime',  # 使用时间
            'number',  # 人数
            'carNumber',  # 车辆数量
            'factoryName',  # 厂别
            'dest',  # 目的地
            'channel',  # 途径地
            'approvalOpinion',
            'departure',  # 出发地
        ]


class Detail2Serializer(serializers.ModelSerializer):
    driverName = serializers.ReadOnlyField(source='driverId.driverName.name', read_only=True)
    driverPhone = serializers.ReadOnlyField(source='driverId.phone', read_only=True)
    licensePlate = serializers.ReadOnlyField(source='carInfoId.licensePlate', read_only=True)
    remark = serializers.ReadOnlyField(source='carInfoId.remark', read_only=True)
    carModel = serializers.ReadOnlyField(source='carInfoId.carModelId.carModel', read_only=True)
    orderNo = serializers.ReadOnlyField(source='assignId.orderNo.orderNo')
    """
    明细表2
    """
    class Meta:
        model = AssignDetail2
        fields = [
            'id',
            'assignId',
            'driverId',
            'carInfoId',
            'driverName',
            'driverPhone',
            'licensePlate',
            'remark',
            'carModel',
            'orderNo'
        ]


class ApplySerializer(serializers.ModelSerializer):
    """
    用车单序列化器
    """
    class Meta:
        model = Apply
        fields = ['id',
                  'orderNo',
                  'orderDate',
                  'userId',
                  'applyDepart',
                  'applyCause',
                  'applyDate',
                  'number',
                  'phone',
                  'departureInfoId',
                  'destId',
                  'carNumber',
                  'carModelId',
                  'factoryId',
                  'useDate',
                  'useTime',
                  'approvalUser',
                  'approvalDate',
                  'approvalOpinion',
                  'approvalStatus',
        ]


class AssignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assign
        fields = [
            'id',
            'internalFeeTotal',
            'marketFeeTotal',
            # 'channel',
        ]
