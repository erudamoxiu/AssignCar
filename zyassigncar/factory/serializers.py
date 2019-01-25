from rest_framework import serializers
from user.models import Factory


class FactoryDetailSerializer(serializers.ModelSerializer):
    """
    厂别详细信息序列化器
    """
    class Meta:
        model = Factory
        fields = ('id', 'factoryName', 'createUser', 'updateUser')
