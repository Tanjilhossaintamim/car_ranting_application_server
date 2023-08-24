from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from .models import User, Client, Owner


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'email', 'password', 'is_owner']


class ClientSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name',
                  'image', 'date_of_birth', 'phone', 'user_id']


class OwnerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Owner
        fields = ['id', 'first_name', 'last_name',
                  'image', 'date_of_birth', 'phone', 'company_name', 'user_id']
