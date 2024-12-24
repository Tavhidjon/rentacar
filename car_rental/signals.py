from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import transaction
from .models import Car, Order
from django.db.models import F

@receiver(post_save, sender=Order)
def update_car_availability(sender, instance, created, **kwargs):
    if created:  
        for car in instance.cars.all():
            car.is_available = False
            car.save()

@receiver(post_save, sender=Order)
def revert_car_availability(sender, instance, **kwargs):
    if not instance.is_available:  
        for car in instance.cars.all():
            car.is_available = True
            car.save()

@receiver(pre_save, sender=Order)
def calculate_order_total_price(sender, instance, **kwargs):
    if instance.days_for_rent and instance.cars.exists():
        total_price = sum(car.price_per_day * instance.days_for_rent for car in instance.cars.all())
        instance.total_price = total_price

