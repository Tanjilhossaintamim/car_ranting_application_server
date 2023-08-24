from rest_framework import serializers
from .models import Car, Catagory, Cart, CartItem


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


class CartItemSerializer(serializers.ModelSerializer):
    car = CarSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'car', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(read_only=True, many=True)
    total_price = serializers.SerializerMethodField(read_only=True)

    def get_total_price(self, cart: Cart):
        return sum([item.quantity*item.car.price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    car_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ['id', 'car_id', 'quantity']

    def validate_car_id(self, car_id):
        if not Car.objects.filter(pk=car_id).exists():
            raise serializers.ValidationError('car does not exists !')
        return car_id

    def save(self, **kwargs):
        car_id = self.validated_data['car_id']
        quantity = self.validated_data['quantity']
        cart_id = self.context.get('cart_id')

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, car_id=car_id)
            # update quantity
            cart_item.quantity += quantity
            self.instance = cart_item.save()
        except CartItem.DoesNotExist:
            # create a cart
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)
        return self.instance


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']
