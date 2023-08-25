import datetime
from django.db import transaction
from rest_framework import serializers
from .models import Car, Catagory, Cart, CartItem, Order, OrderItem


class CatagorySerializer(serializers.ModelSerializer):
    total_car = serializers.IntegerField(read_only=True)

    class Meta:
        model = Catagory
        fields = ['id', 'title', 'total_car']


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


class OrderItemSerializer(serializers.ModelSerializer):
    car = CarSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'car', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'payment_status', 'placed_at', 'user', 'items']


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError({'error': 'cart Is Invalid !'})
        if CartItem.objects.filter(cart_id=cart_id).count() < 1:
            raise serializers.ValidationError({'error': 'Cart Is Empty !'})
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            user_id = self.context.get('user_id')
            try:
                order = Order.objects.get(
                    user_id=user_id, placed_at=datetime.datetime.now().date())
                print('no')
                raise serializers.ValidationError(
                    {'error': 'You Have an existing order in this day !'})
            except Order.DoesNotExist:
                order = Order.objects.create(user_id=user_id)
                cart_items = CartItem.objects.select_related(
                    'car').filter(cart_id=cart_id)

                order_items = [OrderItem(order=order, car=item.car, price=item.car.price,
                                         quantity=item.quantity) for item in cart_items]

                OrderItem.objects.bulk_create(order_items)
                Cart.objects.filter(pk=cart_id).delete()
            return order
