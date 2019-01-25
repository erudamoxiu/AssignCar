from rest_framework import serializers
from user.models import Assign, UEOrderNumber, AssignDetail1, AssignDetail2, CarInfo


class AssignSerializer(serializers.ModelSerializer):
    dest = serializers.ReadOnlyField(source='destFeeId.dest', read_only=True)
    channel = serializers.ReadOnlyField(source='destFeeId.channel', read_only=True)
    APorderNo = serializers.ReadOnlyField(source='orderNo.orderNo', read_only=True)
    """
    派车单序列化器
    """
    class Meta:
        model = Assign
        fields = [
            'id',
            'orderNo',
            'internalFeeTotal',
            'marketFeeTotal',
            'destFeeId',
            'dest',
            'channel',  # 途径地
            'APorderNo',
            'createUser',
            'updateUser',
            'departureDate',
            'departureTime',
        ]


class UeOrderNumberSerializer(serializers.ModelSerializer):
    """
    派车单订单号
    """
    class Meta:
        model = UEOrderNumber
        fields = [
            'id',
            'orderNo',
            'createDate'
        ]


class Detail1Serializer(serializers.ModelSerializer):
    applyUser = serializers.ReadOnlyField(source='applyId.applyUser', read_only=True)
    applyDepart = serializers.ReadOnlyField(source='applyId.applyDepart', read_only=True)
    phone = serializers.ReadOnlyField(source='applyId.phone', read_only=True)
    applyCause = serializers.ReadOnlyField(source='applyId.applyCause', read_only=True)
    useDate = serializers.ReadOnlyField(source='applyId.useDate', read_only=True)
    useTime = serializers.ReadOnlyField(source='applyId.useTime', read_only=True)
    number = serializers.ReadOnlyField(source='applyId.number', read_only=True)
    carNumber = serializers.ReadOnlyField(source='applyId.carNumber', read_only=True)
    approvalStatus = serializers.ReadOnlyField(source='applyId.approvalStatus', read_only=True)
    """
    明细表1
    """
    class Meta:
        model = AssignDetail1
        fields = [
            'id',
            'assignId',
            'applyId',
            'applyUser',
            'applyDepart',
            'phone',
            'applyCause',
            'useDate',
            'useTime',
            'number',
            'carNumber',
            'approvalStatus',
        ]


class Detail2Serializer(serializers.ModelSerializer):
    driverName = serializers.ReadOnlyField(source='driverId.driverName', read_only=True)
    driverPhone = serializers.ReadOnlyField(source='driverId.phone', read_only=True)
    licensePlate = serializers.ReadOnlyField(source='carInfoId.licensePlate', read_only=True)
    remark = serializers.ReadOnlyField(source='carInfoId.remark', read_only=True)
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
            'remark'
        ]


class infoSerializers(serializers.ModelSerializer):

    class Meta:
        model = CarInfo
        fields = [

        ]