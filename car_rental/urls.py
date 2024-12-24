from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'cars', CarViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', CustomerRegistrationView.as_view(), name='register'),
]




