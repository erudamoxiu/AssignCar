from rest_framework import serializers
from user.models import Driver


class DriverSerializer(serializers.ModelSerializer):
    factory_name = serializers.ReadOnlyField(source='factoryId.factoryName', read_only=True)
    name = serializers.ReadOnlyField(source='driverName.name', read_only=True)
    """
    司机详细信息序列化器
    """
    class Meta:
        model = Driver
        fields = ('id', 'driverName',  'phone', 'factoryId', 'factory_name', 'createUser', 'updateUser', 'name')
