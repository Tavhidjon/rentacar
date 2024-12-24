from rest_framework import serializers
from .models import Car, Customer, Order
from django.contrib.auth.models import User
from rest_framework import serializers

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['car_id', 'car_name', 'car_desc', 'price_per_day', 'is_available']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customer_id', 'name', 'email', 'phone', 'address', 'city', 'date_joined']

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    cars = CarSerializer(many=True)

    class Meta:
        model = Order
        fields = ['order_id', 'customer', 'cars', 'days_for_rent', 'rental_date', 'loc_from', 'loc_to', 'total_price']

    def create(self, validated_data):
        customer_data = validated_data.pop('customer')
        cars_data = validated_data.pop('cars')
        customer = Customer.objects.create(**customer_data)
        order = Order.objects.create(customer=customer, **validated_data)
        order.cars.set(cars_data)
        order.save()
        return order




class CustomerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user
