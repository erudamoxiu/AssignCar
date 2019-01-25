from . import models
from rest_framework import serializers


# 定义序列化
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = ('id',
                  'userId',
                  'openId',
                  'name',
                  'persona',
                  'position',
                  'avatar',
                  'jobNumber',
                  'createUser',
                  'updateUser'
        )
