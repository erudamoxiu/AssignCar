import re
from rest_framework import serializers
from user.models import DestFee


class DestFeeSerializer(serializers.ModelSerializer):
    deparTureName = serializers.ReadOnlyField(source='departureInfoId.departure', read_only=True)
    carModel = serializers.ReadOnlyField(source='carModelId.carModel', read_only=True)
    """
    出发地详细信息序列化器
    """
    class Meta:
        model = DestFee
        fields = ('id',
                  'dest',
                  'internalFee',
                  'carModelId',
                  'carModel',
                  'departureInfoId',
                  'deparTureName',
                  'marketFee',
                  'channel',
                  'otherNote',
                  'createUser',
                  'updateUser'
                  )

