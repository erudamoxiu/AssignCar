from rest_framework import serializers
from user.models import CarInfo


class CarInfoSerializer(serializers.ModelSerializer):
    factoryName = serializers.ReadOnlyField(source='factoryId.factoryName', read_only=True)
    carModel = serializers.ReadOnlyField(source='carModelId.carModel', read_only=True)
    driverName = serializers.ReadOnlyField(source='driverId.driverName.name', read_only=True)
    driverPhone = serializers.ReadOnlyField(source='driverId.phone', read_only=True)
    """
    出发地详细信息序列化器
    """
    class Meta:
        model = CarInfo
        fields = ['id',
                  'factoryId',
                  'licensePlate',
                  'carModelId',
                  'number',
                  'driverId',
                  'carFuel',
                  'extraKm',
                  'extraKmPrice',
                  'remark',
                  'factoryName',
                  'carModel',
                  'driverName',
                  'driverPhone',
                  'createUser',
                  'updateUser',
        ]
