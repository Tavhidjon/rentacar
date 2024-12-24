from django.db import models

class Car(models.Model):
    car_id = models.AutoField(primary_key=True)
    car_name = models.CharField(max_length=100, unique=True)
    car_desc = models.TextField(max_length=500, default="")
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    class Meta:
        permissions = [
            ("can_edit_car", "Can edit car details"),
            ("can_view_car", "Can view car details"),
        ]

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name="orders")
    cars = models.ManyToManyField(Car, related_name="orders")
    days_for_rent = models.PositiveIntegerField()
    rental_date = models.DateField(auto_now_add=True)
    loc_from = models.CharField(max_length=100)
    loc_to = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    class Meta:
        permissions = [
            ("can_view_order", "Can view order details"),
            ("can_create_order", "Can create new orders"),
            ("can_manage_order", "Can manage and edit orders"),
        ]

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(max_length=500)
    city = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("can_view_customer", "Can view customer details"),
            ("can_edit_customer", "Can edit customer details"),
        ]
