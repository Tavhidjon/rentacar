from django.apps import AppConfig


class CarRentalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'car_rental'

def ready(self):
        import car_rental.signals