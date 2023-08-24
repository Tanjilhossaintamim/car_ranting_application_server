from rest_framework import serializers
from .models import Car, Catagory


class CatagorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Catagory
        fields = ['id', 'title']


class CarSerializer(serializers.ModelSerializer):
    catagory_id = serializers.IntegerField()
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'title', 'image', 'model',
                  'price', 'catagory_id', 'user_id']

    def validate_catagory_id(self, catagory_id):
        print(catagory_id)
        if Catagory.objects.filter(pk=catagory_id).exists():
            return catagory_id
        raise serializers.ValidationError('Invalid Catagory Id')

    def save(self, **kwargs):
        user_id = self.context.get('user_id')
        if not user_id:
            raise serializers.ValidationError('User Is None !')
        return Car.objects.create(user_id=user_id, **self.validated_data)
