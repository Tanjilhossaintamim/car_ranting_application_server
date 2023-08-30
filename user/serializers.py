from django.conf import settings
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BasedUserSerializer
from rest_framework import serializers
from .models import User, Client, Owner


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'email', 'password', 'is_owner']


class UserSerializer(BasedUserSerializer):
    class Meta(BasedUserSerializer.Meta):
        fields = ['id', 'email', 'is_owner']


class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name',
                  'image', 'date_of_birth', 'phone', 'user']


class OwnerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Owner
        fields = ['id', 'first_name', 'last_name',
                  'image', 'date_of_birth', 'phone', 'company_name', 'user']


class OwnerProfileUpdateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Owner
        fields = ['id', 'first_name', 'last_name',
                  'company_name', 'phone', 'user_id']

    def validate_user_id(self, user_id):
        if Owner.objects.filter(user_id=user_id).exists():
            return user_id
        raise serializers.ValidationError('user id not valid for owner !')

    def save(self, **kwargs):
        user_id = self.validated_data['user_id']
        fist_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        company_name = self.validated_data['company_name']
        phone = self.validated_data['phone']

        owner = Owner.objects.get(user_id=user_id)
        owner.first_name = fist_name
        owner.last_name = last_name
        owner.company_name = company_name
        owner.phone = phone
        self.instance = owner.save()
        return self.instance


class ClientProfileUpdateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'phone', 'user_id']

    def validate_user_id(self, user_id):
        if Client.objects.filter(user_id=user_id).exists():
            return user_id
        raise serializers.ValidationError(
            {'error': 'user id not for client valid !'})

    def save(self, **kwargs):
        user_id = self.validated_data['user_id']
        fist_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        phone = self.validated_data['phone']
        client = Client.objects.get(user_id=user_id)
        client.first_name = fist_name
        client.last_name = last_name
        client.phone = phone
        self.instance = client.save()
        return self.instance
