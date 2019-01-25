from rest_framework import serializers
from user.models import DepartureInfo


class DestDetailSerializer(serializers.ModelSerializer):
    """
    出发地详细信息序列化器
    """
    class Meta:
        model = DepartureInfo
        fields = ('id', 'departure', 'createUser', 'updateUser')
