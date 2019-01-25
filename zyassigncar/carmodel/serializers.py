from rest_framework import serializers
from user.models import CarModel


class CarModelDetailSerializer(serializers.ModelSerializer):
    """
    车型详细信息序列化器
    """
    class Meta:
        model = CarModel
        fields = ('id', 'carModel', 'createUser', 'updateUser')
