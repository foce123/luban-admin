# -*- coding: utf-8 -*-
"""
@Author ：mengying
@Date   ：2024/6/3 17:19
@Email  : 652044581@qq.com
@Desc   : 功能描述
"""
from rest_framework import serializers

from web.models import SystemUser, SystemUserRole, SystemMenu, SystemRole, SystemDept


class SystemUserSerializer(serializers.ModelSerializer):
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = SystemUser
        fields = '__all__'


class SystemDeptSerializer(serializers.ModelSerializer):
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = SystemDept
        fields = '__all__'


class SystemRoleSerializer(serializers.ModelSerializer):
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = SystemRole
        fields = '__all__'


class SystemMenuSerializer(serializers.ModelSerializer):
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = SystemMenu
        fields = '__all__'


class SystemUserRoleSerializer(serializers.ModelSerializer):
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = SystemUserRole
        fields = '__all__'
